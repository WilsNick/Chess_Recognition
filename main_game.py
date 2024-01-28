import os
import cv2
from chess_app_graphics import ChessView
from chess_logic import ChessLogic
from chess_recognition import Chess_Recognition

class ChessApp:
    def __init__(self, url):
        """
        Initializes the ChessApp class with necessary instances and variables.

        Args:
            url (str): Place where the chess feed is located.
        """
        # Instances of Chess_Recognition, ChessLogic, and ChessView
        self.model = Chess_Recognition()
        self.digital_board = ChessLogic()
        self.chess_graphics = ChessView(self)

        # Lists and variables to store game state
        self.move_list = []
        self.move_notation = ""
        self.white_turn = True

        # Variables for image processing and game initialization
        self.picture_old = ""
        self.folder_path = ""
        self.chessboard_initialized = False
        self.started = False
        self.again = False

        # Variables for capturing images
        self.url = url

        self.image_count = 1
        cv2.namedWindow('Captured Image', cv2.WINDOW_NORMAL)
        self.find_game_map()
        self.start_again = False

    def find_game_map(self):
        """
        Finds a suitable path for storing game images.
        """
        folder_main = 'games'
        game_count = 0
        found = False

        while not found:
            game_count += 1
            self.folder_path = f"{folder_main}/game{game_count}"

            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
                print(f"Folder '{self.folder_path}' created successfully.")
                found = True
            else:
                print(f"Folder '{self.folder_path}' already exists.")

    def take_picture(self, picture_name="", startBoard=False):
        """
        Captures and saves a picture from the video feed.

        Args:
            picture_name (str): Custom name for the saved picture. If not provided, a default name is used.
            startBoard (bool): Whether to use the captured image to initialize the chessboard.

        Returns:
            str: Path to the saved image.
        """
        cap = cv2.VideoCapture(self.url)
        ret, frame = cap.read()

        if not ret:
            return None

        if picture_name == "":
            filename = f'move{self.image_count}.jpg'
            self.image_count += 1
        else:
            filename = picture_name

        write_to_path = os.path.join(self.folder_path, filename)
        cv2.imwrite(write_to_path, frame)

        if startBoard:
            cv2.imwrite(filename, frame)

        print(f"Image '{filename}' saved successfully.")
        cv2.imshow('Captured Image', frame)
        cap.release()
        return write_to_path

    def move_piece(self):
        """
        Captures an image, analyzes the board, and makes a move if a legal move is found.
        """
        picture = self.take_picture()

        if picture:
            positions, castle = self.model.check_placement(self.picture_old, picture)

            move = self.digital_board.go_over_top_moves(positions, castle)
            if move is not False:
                self.picture_old = picture

                fen = self.digital_board.print_fen()
                self.move_list.append(move)
                if self.image_count % 2 == 0:
                    self.move_notation += f"{int(self.image_count / 2)}. "
                self.move_notation += f"{move} "
                print(self.move_list)
                print(fen)
                print(self.move_notation)
                pathname = "cropped_image.jpg"
                self.model.get_image(picture, pathname)
                self.chess_graphics.piece_moved(pathname, fen)
            else:
                print("Panic, no legal move")

    def initialize_board(self):
        """
        Initializes the chessboard using a captured image.
        """
        picture = self.take_picture("chessboardEmpty.jpg", not self.start_again)
        if picture:
            if self.start_again:
                picture = "chessboardEmpty.jpg"
            cv_image = cv2.imread(picture)
            cv2.imshow('Captured Image', cv_image)
            cv2.waitKey(1)
            found_board = self.model.initialize_board(picture)
            if found_board:
                pathname = "cropped_image.jpg"
                self.model.get_image(picture, pathname)
                self.chess_graphics.initialized_board(pathname)
                self.picture_old = picture

    def start_placement(self):
        """
        Fills the chessboard based on a captured image.
        """
        picture = self.take_picture("chessboardFull.jpg")
        if picture:
            cv_image = cv2.imread(picture)
            cv2.imshow('Captured Image', cv_image)
            cv2.waitKey(1)
            self.model.fill_board(picture)
            self.model.initialize_board(self.picture_old, False)
            pathname = "cropped_image.jpg"
            self.model.get_image(picture, pathname)
            self.chess_graphics.start_placed(pathname)
            self.picture_old = picture
            self.started = True

    def reset(self):
        """
        Resets the game state but use the same board initialization next game.
        Camera can not be moved in between
        """
        self.again = True

    def run(self, reset):
        """
        Main loop for running the chess application.

        Args:
            reset (bool): Indicates whether to reset the game.

        Returns:
            bool: True if the application should continue running, False otherwise.
        """
        if reset:
            self.start_again = True
        self.chess_graphics.run()
        if self.again:
            return True
        return False


if __name__ == "__main__":
    running = True
    reset = False
    url = "http://192.168.0.106:4747/video"
    while running:
        app = ChessApp(url)
        running = app.run(reset)
        reset = True
