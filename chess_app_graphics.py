import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk

class ChessView:
    def __init__(self, model):
        """
        ChessView constructor.

        Args:
            model (ChessLogic): An instance of the ChessLogic class.
        """
        self.model = model

        root = tk.Tk()
        self.root = root

        self.root.title("Chessboard App")

        # Create GUI components
        self.initialize_button = tk.Button(root, text="Initialize Board", command=self.model.initialize_board)
        self.initialize_button.grid(row=0, column=0, columnspan=2, pady=10)

        self.fill_button = tk.Button(root, text="Fill the board", command=self.model.start_placement)

        # Create a label for displaying the captured image
        self.captured_image_label = tk.Label(root)
        self.captured_image_label.grid(row=1, column=0, padx=10, pady=10)

        self.digital_board_image = tk.Label(root)
        self.digital_board_image.grid(row=1, column=1, padx=10, pady=10)

        # Create stopwatch buttons
        self.white_timer_button = tk.Button(root, text="White Timer: 10:00", font=("Helvetica", 16),
                                            command=self.model.move_piece, height=25, width=50)
        self.white_timer_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        # Deactivate the button
        self.white_timer_button["state"] = "disabled"
        self.white_timer_button.configure(bg="gray")

        self.black_timer_button = tk.Button(root, text="Black Timer: 10:00", font=("Helvetica", 16),
                                            command=self.model.move_piece, height=25, width=50)
        self.black_timer_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        # Deactivate the button
        self.black_timer_button["state"] = "disabled"
        self.black_timer_button.configure(bg="gray")

        self.space_move = self.root.bind("<space>", lambda event: self.space_pressed())
        self.r_reset = self.root.bind("<r>", lambda event: self.reset())
        # Initialize variables for stopwatch
        self.start_time_white = 0
        self.start_time_black = 0
        self.current_player = "white"

        self.duration = 600  # 10 minutes in seconds
        self.duration_white = 600  # 10 minutes in seconds
        self.duration_black = 600  # 10 minutes in seconds

        # Update the stopwatch buttons periodically
        self.root.after(100, self.update_chess_clocks)

        # Label for restart instructions
        self.restart_label = tk.Label(root, text='Press "r" to restart the game with the same board position. You can then just press Initialize board without clearing the board.')
        self.restart_label.grid(row=3, column=0, columnspan=2, pady=10)


    def reset(self):
        """
        Reset the chessboard and close the application to restart it.
        """
        self.model.reset()
        self.root.destroy()

    def piece_moved(self, pathname, fen):
        """
        Update the GUI when a piece is moved.

        Args:
            pathname (str): The path to the image file.
            fen (str): FEN notation representing the current chessboard state.
        """
        self.draw_pictures(pathname, fen)
        if self.current_player == "white":
            self.white_moved()
        else:
            self.black_moved()

    def space_pressed(self):
        """
        Handle spacebar press event to move a piece.
        """
        if self.model.started:
            return self.model.move_piece()

    def draw_pictures(self, pathname, fen):
        """
        Draw images on the GUI based on the provided information.

        Args:
            pathname (str): The path to the image file.
            fen (str): FEN notation representing the current chessboard state.
        """
        cv_image = cv2.imread(pathname)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        img = img.resize((400, 400))
        img = ImageTk.PhotoImage(img)
        self.captured_image_label.config(image=img)
        self.captured_image_label.photo_image = img

        photo_image = self.draw_chessboard(fen)
        self.digital_board_image.config(image=photo_image)
        self.digital_board_image.photo_image = photo_image

    def white_moved(self):
        """
        Handle actions when white player makes a move.
        """
        self.start_time_black = time.time()
        self.current_player = "black"

        self.black_timer_button.configure(bg="green")
        self.black_timer_button["state"] = "normal"

        self.white_timer_button.configure(bg="gray")
        self.white_timer_button["state"] = "disabled"

    def black_moved(self):
        """
        Handle actions when black player makes a move.
        """
        self.start_time_white = time.time()
        self.current_player = "white"

        self.white_timer_button.configure(bg="green")
        self.white_timer_button["state"] = "normal"

        self.black_timer_button.configure(bg="gray")
        self.black_timer_button["state"] = "disabled"

    def update_chess_clocks(self):
        """
        Update the chess clocks for the players turn.
        """
        # Update the left chess clock
        if self.start_time_white and self.current_player == "white":
            elapsed_time_white = time.time() - self.start_time_white
            remaining_time_white = max(self.duration_white - elapsed_time_white, 0)
            minutes_left_white = int(remaining_time_white / 60)
            seconds_left_white = int(remaining_time_white % 60)

            self.duration_white = remaining_time_white
            self.start_time_white = time.time()
            self.white_timer_button.config(text=f"White Timer: {minutes_left_white:02d}:{seconds_left_white:02d}")

        # Update the right chess clock
        if self.start_time_black and self.current_player == "black":
            elapsed_time_black = time.time() - self.start_time_black
            remaining_time_black = max(self.duration_black - elapsed_time_black, 0)
            minutes_left_black = int(remaining_time_black / 60)
            seconds_left_black = int(remaining_time_black % 60)

            self.duration_black = remaining_time_black
            self.start_time_black = time.time()
            self.black_timer_button.config(text=f"Black Timer: {minutes_left_black:02d}:{seconds_left_black:02d}")

        # Call the update function again after 1000 milliseconds (1 second)
        self.root.after(1000, self.update_chess_clocks)

    def draw_chessboard(self, fen):
        """
        Draw the chessboard on the GUI based on the FEN notation.

        Args:
            fen (str): FEN notation representing the current chessboard state.

        Returns:
            PhotoImage: The PhotoImage of the chessboard with pieces.
        """
        location = "img/"
        chessboard = Image.open(location + "chessboard.png").convert("RGBA")
        chessboard = chessboard.resize((400, 400))

        pieces = {
            'r': location + 'black_rook.png',
            'n': location + 'black_knight.png',
            'b': location + 'black_bishop.png',
            'q': location + 'black_queen.png',
            'k': location + 'black_king.png',
            'p': location + 'black_pawn.png',
            'R': location + 'white_rook.png',
            'N': location + 'white_knight.png',
            'B': location + 'white_bishop.png',
            'Q': location + 'white_queen.png',
            'K': location + 'white_king.png',
            'P': location + 'white_pawn.png'
        }

        image = Image.new("RGBA", (400, 400), (0, 0, 0, 0))

        # Paste the chessboard onto the final image
        image.paste(chessboard, (0, 0), chessboard)
        rank = 0
        file = 0
        fen = fen.split()
        fen = fen[0]
        for char in fen:
            if char == '/':
                rank += 1
                file = 0
            elif char.isdigit():
                file += int(char)
            else:
                piece_image = Image.open(pieces[char]).convert("RGBA")
                piece_image = piece_image.resize((50, 50))

                # Paste the piece onto the chessboard
                box = (file * 50, rank * 50)
                image.paste(piece_image, box, piece_image)

                file += 1

        return ImageTk.PhotoImage(image)

    def initialized_board(self, pathname):
        """
        Display the initialized chessboard state on the GUI.

        Args:
            pathname (str): The path to the image file.
        """
        fen_notation = "8/8/8/8/8/8/8/8"
        self.draw_pictures(pathname, fen_notation)

        self.initialize_button.grid_remove()
        self.fill_button.grid(row=0, column=0, columnspan=2, pady=10)

    def start_placed(self, pathname):
        """
        Display the chessboard with pieces at the start of the game on the GUI.

        Args:
            pathname (str): The path to the image file.
        """
        fen_notation = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.draw_pictures(pathname, fen_notation)

        self.fill_button.grid_remove()
        self.white_timer_button.configure(bg="green")
        self.white_timer_button["state"] = "normal"

    def run(self):
        """
        Run the main GUI loop.
        """
        self.root.mainloop()
