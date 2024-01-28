import math

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


class Chess_Recognition:
    def __init__(self):
        """
        Chess_Recognition constructor.
        Initializes instance variables for height, width, rotation, and coordinates.
        """
        self.height = 0
        self.width = 0
        self.rotation = 0
        self.coordinates = None

    def rotate_image(self, image):
        """
        Rotate the given image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            numpy.ndarray: The rotated image.
        """
        # Get image center
        height, width = image.shape[:2]
        center = (width // 2, height // 2)

        # Define the rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, self.rotation, 1.0)

        # Find the new dimensions of the rotated image
        new_width = int(np.ceil(width * np.abs(np.cos(np.radians(self.rotation)))) + np.ceil(
            height * np.abs(np.sin(np.radians(self.rotation)))))
        new_height = int(np.ceil(width * np.abs(np.sin(np.radians(self.rotation)))) + np.ceil(
            height * np.abs(np.cos(np.radians(self.rotation)))))

        # Apply the rotation to the image
        rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height), flags=cv2.INTER_LINEAR)

        return rotated_image

    def fill_board(self, image_path):
        """
        Fill the chessboard based on image rotation.

        Args:
            image_path (str): Path to the input image.
        """
        # Load the chessboard image
        image = cv2.imread(image_path)

        if self.rotation != 0:
            image = self.rotate_image(image)

        first_row = 0
        first_col = 0
        last_row = 0
        last_col = 0
        for i in range(8):
            for j in range(8):
                cell_corners = self.coordinates[i][j]
                x, y = map(int, cell_corners)

                # Extract the cell from the original image
                cell = image[y:y + self.height, x:x + self.width]

                # Calculate the average color in the cell
                average_color = cv2.mean(cell)

                sum_colors = average_color[0] + average_color[1] + average_color[2]
                if i == 1 or i == 0:
                    first_row += sum_colors
                if i == 6 or i == 7:
                    last_row += sum_colors
                if j == 1 or j == 0:
                    first_col += sum_colors
                if j == 6 or j == 7:
                    last_col += sum_colors

        rows = abs(abs(first_row) - abs(last_row))
        cols = abs(abs(first_col) - abs(last_col))
        if rows > cols:
            if first_row > last_row:
                max_index = 0
            else:
                max_index = 2
        else:
            if first_col > last_col:
                max_index = 1
            else:
                max_index = 3
        self.rotation += max_index * 90
        return

    def initialize_board(self, image_path, loop_prevention=True):
        """
        Initialize the chessboard by detecting corners and calculating rotation.

        Args:
            image_path (str): Path to the input image.
            loop_prevention (bool): Flag for loop prevention in case of multiple iterations.

        Returns:
            bool: True if initialization is successful, False otherwise.
        """
        # Load the chessboard image

        image = cv2.imread(image_path)

        if self.rotation != 0:
            image = self.rotate_image(image)
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Define the chessboard size
        chessboard_size = (7, 7)

        # Find chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
        # If corners are found, draw them on the image and save coordinates
        if ret:

            # Reshape the corners array to match the chessboard structure
            corners = corners.reshape(-1, 2)

            # Organize the corners into a list of lists
            cell_coordinates = []
            for i in range(chessboard_size[1]):
                row_coordinates = []
                for j in range(chessboard_size[0]):
                    index = i * chessboard_size[0] + j
                    row_coordinates.append(corners[index].tolist())
                cell_coordinates.append(row_coordinates)

            height = (cell_coordinates[1][1][0] - cell_coordinates[2][2][0])
            width = (cell_coordinates[1][1][1] - cell_coordinates[2][2][1])

            # way to add the eight row and column

            placeheight = 0
            newplaceheight = 1
            posheight = False
            if height > 0:
                posheight = True
                placeheight = -1
                newplaceheight = -2
                height = -height

            poswidth = False
            placewidth = 0
            newplacewidth = 0
            if width > 0:
                placewidth = len(cell_coordinates[0]) - 1
                newplacewidth = len(cell_coordinates[0])
                poswidth = True
                width = -width

            if posheight:
                cell_coordinates.append([])
            else:
                cell_coordinates.insert(0, [])

            for i in range(7):
                x, y = cell_coordinates[newplaceheight][i]
                y = y + height
                newcell = [x, y]
                cell_coordinates[placeheight].append(newcell)

            for i in range(8):
                x, y = cell_coordinates[i][placewidth]
                x = x + width
                newcell = [x, y]
                cell_coordinates[i].insert(newplacewidth, newcell)

            if poswidth:
                for i in range(8):
                    cell_coordinates[i] = list(reversed(cell_coordinates[i]))

            if not posheight:
                cell_coordinates = list(reversed(cell_coordinates))

            height2 = (cell_coordinates[1][1][0] - cell_coordinates[6][6][0])
            width2 = (cell_coordinates[1][1][1] - cell_coordinates[6][6][1])
            # Calculate the rotation angle in radians
            rotation_angle_rad = math.atan2(width2, height2)
            # Convert radians to degrees
            rotation_angle_deg = math.degrees(rotation_angle_rad)

            if loop_prevention:
                self.rotation = rotation_angle_deg + 45 + self.rotation
                return self.initialize_board(image_path, False)
            else:
                self.height = -int(height)
                self.width = -int(width)
                self.coordinates = cell_coordinates
                return True
        else:
            print("Chessboard not found in the image.")
        return False

    def get_image(self, image_path, pathname=""):
        """
        Retrieve an image with potential rotation applied.

        Args:
            image_path (str): Path to the input image.
            pathname (str): Path to save the resulting image.
        """
        image = cv2.imread(image_path)

        if self.rotation != 0:
            image = self.rotate_image(image)

        self.showImage(image, pathname)

    def showImage(self, image, pathname=""):
        """
        Display or save the image.

        Args:
            image (numpy.ndarray): The input image.
            pathname (str): Path to save the resulting image.
        """
        if pathname == "":
            pathname = "cropped_image.jpg"
        cell_corners = self.coordinates[0][0]
        x, y = map(int, cell_corners)
        image = image[int(y - 7.5 * self.height): int(y + 1.5 * self.height),
                int(x - self.width * 0.5): int(x + self.width * 8.5)]
        cv2.imwrite(pathname, image)

    def calculate_color_difference(self, cell_old, cell):
        """
        Calculate the color difference between two cells.

        Args:
            cell_old (numpy.ndarray): First cell.
            cell (numpy.ndarray): Second cell.

        Returns:
            float: Color difference.
        """
        return np.sum(np.abs(np.asarray(cell_old, dtype=np.int32) - np.asarray(cell, dtype=np.int32))) / (
                cell_old.shape[0] * cell_old.shape[1])

    def calculate_ssim(self, cell_old, cell):
        """
        Calculate the Structural Similarity Index (SSIM) between two cells.

        Args:
            cell_old (numpy.ndarray): First cell.
            cell (numpy.ndarray): Second cell.

        Returns:
            float: SSIM.
        """
        return ssim(cell_old, cell, full=True)[0]

    def detect_movement(self, des_old, des):
        """
        Detect movement using feature matching.

        Args:
            des_old (numpy.ndarray): Descriptors for the old cell.
            des (numpy.ndarray): Descriptors for the new cell.

        Returns:
            list: List of good matches.
        """
        bf = cv2.BFMatcher()
        des_old = des_old.astype(np.float32)
        des = des.astype(np.float32)
        matches = bf.knnMatch(des_old, des, k=2)
        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:  # Check if there are two matches
                m, n = match_pair
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)
        return good_matches

    def remove_duplicates(self, src_pts, dst_pts):
        """
        Remove duplicate points in feature matching.

        Args:
            src_pts (numpy.ndarray): Source points.
            dst_pts (numpy.ndarray): Destination points.

        Returns:
            tuple: Unique source and destination points.
        """
        unique_indices = np.unique(src_pts, axis=0, return_index=True)[1]
        src_pts = src_pts[unique_indices]
        dst_pts = dst_pts[unique_indices]
        return src_pts, dst_pts

    def check_placement(self, image_path_old, image_path, test=False):
        """
        Check for piece movement and potential castling.

        Args:
            image_path_old (str): Path to the old chessboard image.
            image_path (str): Path to the new chessboard image.
            test (bool): Flag for test mode.

        Returns:
            tuple: List of top differences and a flag indicating castling.
        """
        # Constants
        crop_percentage = 0.1
        threshold = 10
        top_cells_count = 10
        # Load the chessboard images

        image_old = cv2.imread(image_path_old)

        if self.rotation != 0:
            image_old = self.rotate_image(image_old)

        image = cv2.imread(image_path)

        if self.rotation != 0:
            image = self.rotate_image(image)

        # Convert the images to grayscale
        gray_old = cv2.cvtColor(image_old, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Initialize SIFT detector
        sift = cv2.SIFT_create()

        # List to store top differences and their positions
        top_diffs = [(0, 0)] * top_cells_count

        # List to store results for each cell
        cell_results = []

        for i in range(8):
            for j in range(8):
                cell_corners = self.coordinates[i][j]
                x, y = map(int, cell_corners)

                cell_old = gray_old[y:y + self.height, x:x + self.width]
                cell = gray[y:y + self.height, x:x + self.width]

                crop_x = int(self.width * crop_percentage)
                crop_y = int(self.height * crop_percentage)
                cell_cropped_old = cell_old[crop_y: self.height - crop_y, crop_x: self.width - crop_x]
                cell_cropped = cell[crop_y: self.height - crop_y, crop_x: self.width - crop_x]

                color_difference = self.calculate_color_difference(cell_old, cell)
                similarity_index = self.calculate_ssim(cell_old, cell)

                combined_score = 0.5 * (color_difference / (self.height * self.width)) + 0.5 * (1 - similarity_index)

                kp_old, des_old = sift.detectAndCompute(cell_cropped_old, None)
                kp, des = sift.detectAndCompute(cell_cropped, None)

                amount_good_matches = 0

                if des_old is not None and des is not None:
                    good_matches = self.detect_movement(des_old, des)

                    src_pts, dst_pts = self.remove_duplicates(
                        np.float32([kp_old[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2),
                        np.float32([kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2))
                    src_pts, dst_pts = self.remove_duplicates(dst_pts, src_pts)
                    inliers = len(src_pts)

                    if test:
                        print("amount of true matches", inliers)

                    movement_detected = inliers > threshold
                    cell_results.append(movement_detected)

                    amount_good_matches = inliers

                else:
                    good_matches = []

                if test:
                    print("cell", i, j, "score", combined_score, "all matches", len(good_matches))

                difference = combined_score - 0.03 * len(good_matches)

                if amount_good_matches < 5:
                    # Compare with the top differences
                    for idx, (top_diff, top_pos) in enumerate(top_diffs):
                        if difference > top_diff:
                            top_diffs.insert(idx, (difference, (i, j)))
                            top_diffs.pop()
                            break

        # calculate if castling
        long_c_0 = [0, 2, 3, 4]
        short_c_0 = [4, 5, 6, 7]
        long_c_7 = [0, 2, 3, 4]
        short_c_7 = [4, 5, 6, 7]
        for diff, pos in top_diffs:
            if pos[0] == 0:
                if pos[1] in short_c_0:
                    short_c_0.remove(pos[1])
                if pos[1] in long_c_0:
                    long_c_0.remove(pos[1])

            if pos[0] == 7:
                if pos[1] in short_c_7:
                    short_c_7.remove(pos[1])
                if pos[1] in long_c_7:
                    long_c_7.remove(pos[1])

        castle = False
        if len(short_c_0) == 0 or len(long_c_0) == 0:
            castle = True
            x_pos = 0
            if len(short_c_0):
                y0_pos = 4
                y1_pos = 0
            else:
                y0_pos = 4
                y1_pos = 7

            return [(x_pos, y0_pos), (x_pos, y1_pos)], castle

        if len(short_c_7) == 0 or len(long_c_7) == 0:
            castle = True
            x_pos = 7
            if len(short_c_7):
                y0_pos = 4
                y1_pos = 0
            else:
                y0_pos = 4
                y1_pos = 7

            return [(x_pos, y0_pos), (x_pos, y1_pos)], castle

        # if not castling
        return top_diffs, castle
