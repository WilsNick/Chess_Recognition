class ChessLogic:
    def __init__(self):
        """
        Initializes the ChessLogic class with an initial chessboard configuration.
        """
        # Initial chessboard configuration
        self.chess_board = [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["", "", "", "", "", "", "", ""],  # Empty row
            ["", "", "", "", "", "", "", ""],  # Empty row
            ["", "", "", "", "", "", "", ""],  # Empty row
            ["", "", "", "", "", "", "", ""],  # Empty row
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "q", "k", "b", "n", "r"]
        ]

        self.white_turn = True

        # Initial game state variables
        self.castling_rights = "KQkq"
        self.en_passant = "-"
        self.halfmove_clock = 0
        self.fullmove_number = 0

    def is_white_piece(self, piece):
        """
        Checks if a given piece is white.

        Args:
            piece (str): The piece to check.

        Returns:
            bool: True if the piece is white, False otherwise.
        """
        return piece.isupper()

    def is_black_piece(self, piece):
        """
        Checks if a given piece is black.

        Args:
            piece (str): The piece to check.

        Returns:
            bool: True if the piece is black, False otherwise.
        """
        return piece.islower()

    def is_valid_move(self, start_pos, end_pos):
        """
        Checks if a move from start_pos to end_pos is valid.

        Args:
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        if start_pos == end_pos:
            return False
        # Check if the move is legal without considering the king's safety
        if not self.is_valid_piece_move(start_pos, end_pos):
            return False
        # Check if the piece at the starting position belongs to the current player
        if (self.white_turn and not self.is_white_piece(self.chess_board[start_row][start_col])) or \
                (not self.white_turn and not self.is_black_piece(self.chess_board[start_row][start_col])):
            return False
        # Check if the ending position is not occupied by a piece of the same color
        if (self.white_turn and self.is_white_piece(self.chess_board[end_row][end_col])) or \
                (not self.white_turn and self.is_black_piece(self.chess_board[end_row][end_col])):
            return False
        # Make a hypothetical move on a copy of the board
        hypothetical_board = [row[:] for row in self.chess_board]
        self.move_piece(hypothetical_board, start_pos, end_pos)

        # Check if the player's own king is in check after the move
        king_position = self.find_king_position(self.white_turn)
        if self.is_in_check(hypothetical_board, king_position, self.white_turn):
            return False

        return True

    def move_piece(self, chess_board, start_pos, end_pos):
        """
        Moves a piece on the given chess_board from start_pos to end_pos.

        Args:
            chess_board (list): The chessboard configuration.
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        chess_board[end_row][end_col] = chess_board[start_row][start_col]
        chess_board[start_row][start_col] = ""

    def find_king_position(self, is_white, board=None):
        """
        Finds the position of the king on the chessboard.

        Args:
            is_white (bool): True if searching for the white king, False for the black king.
            board (list): Optional chessboard configuration.

        Returns:
            tuple: The position (row, col) of the king.
        """
        if board is None:
            board = self.chess_board
        king_symbol = "K" if is_white else "k"

        for row in range(8):
            for col in range(8):
                if board[row][col] == king_symbol:
                    return (row, col)

    def is_in_check(self, chess_board, king_position, is_white):
        """
        Checks if the king is in check on the given chessboard.

        Args:
            chess_board (list): The chessboard configuration.
            king_position (tuple): The position (row, col) of the king.
            is_white (bool): True if checking for white king, False for black king.

        Returns:
            bool: True if the king is in check, False otherwise.
        """
        # Check if the king is under attack by any opponent's piece
        for row in range(8):
            for col in range(8):
                if self.is_opponent_piece(chess_board[row][col], is_white) and \
                        self.is_valid_piece_move((row, col), king_position):
                    return True

        return False

    def is_opponent_piece(self, piece, is_white):
        """
        Checks if a piece belongs to the opponent.

        Args:
            piece (str): The piece to check.
            is_white (bool): True if checking for the white opponent, False for the black opponent.

        Returns:
            bool: True if the piece belongs to the opponent, False otherwise.
        """
        # Check if a piece belongs to the opponent (one is uppercase and the other is lowercase)
        return (piece.islower() and is_white) or (piece.isupper() and not is_white)

    def is_valid_piece_move(self, start_pos, end_pos):
        """
        Checks if a piece can legally move from start_pos to end_pos.

        Args:
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).

        Returns:
            bool: True if the move is valid for the piece, False otherwise.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        # print(start_pos)
        piece = self.chess_board[start_row][start_col].lower()
        is_white = self.chess_board[start_row][start_col].isupper()

        # Determine the possible moves based on the piece type
        if piece == 'p':
            return self.is_valid_pawn_move(start_pos, end_pos, is_white)
        elif piece == 'r':
            return self.is_valid_rook_move(start_pos, end_pos)
        elif piece == 'n':
            return self.is_valid_knight_move(start_pos, end_pos)
        elif piece == 'b':
            return self.is_valid_bishop_move(start_pos, end_pos)
        elif piece == 'q':
            return self.is_valid_queen_move(start_pos, end_pos)
        elif piece == 'k':
            return self.is_valid_king_move(start_pos, end_pos)
        else:
            # Unknown piece type
            return False

    def is_valid_pawn_move(self, start_pos, end_pos, is_white):
        """
        Checks if a pawn move from start_pos to end_pos is valid.

        Args:
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).
            is_white (bool): True if it's a white pawn, False for a black pawn.

        Returns:
            bool: True if the pawn move is valid, False otherwise.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        direction = 1 if is_white else -1

        # Check standard pawn move (one square forward)
        if start_col == end_col and start_row + direction == end_row and self.chess_board[end_row][end_col] == "":
            return True

        # Check initial double move for pawns
        if start_col == end_col and start_row + 2 * direction == end_row and \
                ((is_white and start_row == 1) or (not is_white and start_row == 6)) and \
                self.chess_board[start_row + direction][end_col] == "" and self.chess_board[end_row][end_col] == "":
            return True

        # Check capturing diagonally
        if abs(start_col - end_col) == 1 and start_row + direction == end_row:
            # Check if the move captures an opponent's piece
            if self.is_opponent_piece(self.chess_board[start_row][start_col], is_white) and \
                    self.chess_board[end_row][end_col] != "":
                return True

            # Check en passant
            if self.en_passant == chr(ord('a') + end_col) + str(end_row + 1):
                return True

        return False

    def is_valid_rook_move(self, start_pos, end_pos):
        """
        Checks if a rook move from start_pos to end_pos is valid.

        Args:
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).

        Returns:
            bool: True if the rook move is valid, False otherwise.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Check if moving along a row or column
        if start_row == end_row or start_col == end_col:
            # Check if the path is clear
            return self.is_clear_path(start_pos, end_pos)

        return False

    def is_valid_knight_move(self, start_pos, end_pos):
        """
        Checks if a knight move from start_pos to end_pos is valid.

        Args:
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).

        Returns:
            bool: True if the knight move is valid, False otherwise.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Check if moving in an L-shape (2 squares in one direction and 1 square in the other)
        return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
            (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)

    def is_valid_bishop_move(self, start_pos, end_pos):
        """
        Checks if a bishop move from start_pos to end_pos is valid.

        Args:
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).

        Returns:
            bool: True if the bishop move is valid, False otherwise.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Check if moving along a diagonal
        if abs(start_row - end_row) == abs(start_col - end_col):
            # Check if the path is clear
            return self.is_clear_path(start_pos, end_pos)

        return False

    def is_valid_queen_move(self, start_pos, end_pos):
        """
        Checks if a queen move from start_pos to end_pos is valid.

        Args:
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).

        Returns:
            bool: True if the queen move is valid, False otherwise.
        """
        # Queen can move like a rook or a bishop
        return self.is_valid_rook_move(start_pos, end_pos) or self.is_valid_bishop_move(start_pos, end_pos)

    def is_valid_king_move(self, start_pos, end_pos):
        """
        Checks if a king move from start_pos to end_pos is valid.

        Args:
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).

        Returns:
            bool: True if the king move is valid, False otherwise.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Check if moving only one square in any direction
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

    def is_clear_path(self, start_pos, end_pos):
        """
        Checks if the path between start_pos and end_pos is clear of other pieces.

        Args:
            start_pos (tuple): The starting position (row, col).
            end_pos (tuple): The ending position (row, col).

        Returns:
            bool: True if the path is clear, False otherwise.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Check if the path is clear in rows or columns
        if start_row == end_row:
            for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                if self.chess_board[start_row][col] != "":
                    return False
        elif start_col == end_col:
            for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                if self.chess_board[row][start_col] != "":
                    return False
        else:
            # Check if the path is clear diagonally
            row_dir = 1 if end_row > start_row else -1
            col_dir = 1 if end_col > start_col else -1
            row, col = start_row + row_dir, start_col + col_dir
            while (row, col) != (end_row, end_col):
                if self.chess_board[row][col] != "":
                    return False
                row += row_dir
                col += col_dir

        return True

    def print_fen(self):
        """
        Converts the current chessboard configuration to Forsyth-Edwards Notation (FEN).

        Returns:
            str: The FEN representation of the chessboard.
        """
        fen = ""

        # Convert the chess board to FEN string
        for row in list(reversed(self.chess_board)):
            empty_count = 0
            for piece in row:
                if piece == "":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += piece

            if empty_count > 0:
                fen += str(empty_count)
            fen += "/"

        # Remove the trailing "/"
        fen = fen[:-1]

        # Add turn indicator
        fen += " " + ("w" if self.white_turn else "b")

        # Add castling rights
        fen += " " + self.castling_rights

        # Add en passant target square
        fen += " " + self.en_passant

        # Add halfmove clock and fullmove number
        fen += f" {self.halfmove_clock} {self.fullmove_number}"

        return fen

    def go_over_top_moves(self, positions, castle):
        """
        Go over all the pair options in positions to find the most probable legal move.
        Update the board if a legal move is found.
        Checks and updates the chessboard based on the provided positions.

        Args:
            positions (list): List of board positions (tuples).
            castle (bool): True if it's a castling move.

        Returns:
            str or False: The move notation if successful, False otherwise.
        """
        if castle:
            pair1 = (positions[0][0], positions[0][1])
            pair2 = (positions[1][0], positions[1][1])
            return self.update_chessboard(pair1, pair2, True)
        pairs = []
        for i in range(1, len(positions)):
            for j in range(i):
                if j < len(positions):
                    pairs.append((positions[j][1], positions[i][1]))

        for pair in pairs:
            pair1 = (pair[0][0], pair[0][1])
            pair2 = (pair[1][0], pair[1][1])
            valid = self.is_valid_move(pair1, pair2)
            if valid:
                return self.update_chessboard(pair1, pair2, False)
            valid = self.is_valid_move(pair2, pair1)
            if valid:
                return self.update_chessboard(pair2, pair1, False)
        return False

    def update_chessboard(self, pos1, pos2, castle):
        """
        Updates the chessboard based on the provided positions.

        Args:
            pos1 (tuple): The starting position (row, col).
            pos2 (tuple): The ending position (row, col).
            castle (bool): True if it's a castling move.

        Returns:
            str: The move notation.
        """
        # Extracting row and column from the positions
        row1, col1 = pos1
        row2, col2 = pos2

        switchPiece = False
        # Getting the piece and destination square
        piece = self.chess_board[row1][col1]
        destination_square = self.chess_board[row2][col2]
        capture = ""
        if castle:
            king = "K"
            rook = "R"
            if self.white_turn:
                self.castling_rights = self.castling_rights.replace('K', '')
                self.castling_rights = self.castling_rights.replace('Q', '')
            else:
                king = "k"
                rook = "r"
                self.castling_rights = self.castling_rights.replace('k', '')
                self.castling_rights = self.castling_rights.replace('q', '')
            if col1 == 0 or col2 == 0:

                self.chess_board[row1][2] = king
                self.chess_board[row1][3] = rook
                self.chess_board[row1][0] = ""
                self.chess_board[row1][4] = ""

                notation = "0-0"
            else:

                self.chess_board[row1][6] = king
                self.chess_board[row1][5] = rook
                self.chess_board[row1][7] = ""
                self.chess_board[row1][4] = ""

                notation = "0-0-0"
        else:
            if piece:
                if self.white_turn and not piece.isupper():
                    switchPiece = True

                if not self.white_turn and piece.isupper():
                    switchPiece = True
            else:
                switchPiece = True

            if switchPiece:
                row1, col1 = pos2
                row2, col2 = pos1
                piece = self.chess_board[row1][col1]
                destination_square = self.chess_board[row2][col2]

            if self.white_turn:
                if (row1, col1) == (0, 0):
                    self.castling_rights = self.castling_rights.replace('K', '')
                if (row1, col1) == (0, 7):
                    self.castling_rights = self.castling_rights.replace('Q', '')
                if (row1, col1) == (0, 3):
                    self.castling_rights = self.castling_rights.replace('K', '')
                    self.castling_rights = self.castling_rights.replace('Q', '')
            else:
                if (row1, col1) == (7, 0):
                    self.castling_rights = self.castling_rights.replace('k', '')
                if (row1, col1) == (7, 7):
                    self.castling_rights = self.castling_rights.replace('q', '')
                if (row1, col1) == (7, 3):
                    self.castling_rights = self.castling_rights.replace('k', '')
                    self.castling_rights = self.castling_rights.replace('q', '')

            # Determine if the move is a capture
            capture = "x" if destination_square else ""
            move_piece = ""
            # If the piece is a pawn and the move is a capture, include the source column in the notation
            if piece.lower() == 'p' and capture:
                move_piece = chr(ord('a') + col1)
            elif piece.lower() != 'p':
                move_piece = piece.upper()
            destination_move = chr(ord('a') + col2) + str(row2 + 1)

            notation = move_piece + capture + destination_move
            # Update the chessboard
            self.chess_board[row2][col2] = piece
            self.chess_board[row1][col1] = ""

        self.white_turn = not self.white_turn
        king_position = self.find_king_position(self.white_turn)
        if self.is_checkmate(self.white_turn):
            notation += "# "
            if self.white_turn:
                notation += "0-1"
            else:
                notation += "1-0"
        elif self.is_in_check(self.chess_board, king_position, self.white_turn):
            notation += "+"

        if self.castling_rights == "":
            self.castling_rights = "-"

        if piece.lower() == "p" or capture:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        self.en_passant = '-'
        if piece.lower() == "p":
            if row1 == 1 and row2 == 3:
                self.en_passant = chr(ord('a') + col2) + str(row2 + 1)
            if row1 == 6 and row2 == 4:
                self.en_passant = chr(ord('a') + col2) + str(row2 + 1)
        if self.white_turn:
            self.fullmove_number += 1
        return notation

    def is_checkmate(self, white_turn):
        """
        Checks if the current player is in checkmate.

        Args:
            white_turn (bool): True if it's white's turn, False otherwise.

        Returns:
            bool: True if the current player is in checkmate, False otherwise.
        """
        king_position = self.find_king_position(white_turn)
        # Check if the player's own king is in check after the move
        if self.is_in_check(self.chess_board, king_position, white_turn):

            # Iterate through all pieces on the board
            for row in range(8):
                for col in range(8):
                    piece = self.chess_board[row][col]

                    # Check if the piece belongs to the current player
                    if (piece.isupper() and white_turn) or (piece.islower() and not white_turn):
                        # Iterate through all possible moves for the current piece
                        for target_row in range(8):
                            for target_col in range(8):
                                if self.is_valid_move((row, col), (target_row, target_col)):
                                    return False  # If at least one legal move is found, it's not checkmate
        else:
            return False
        return True  # If no legal moves are found for any piece, it's checkmate


if __name__ == '__main__':
    # Example usage:
    chess_game = ChessLogic()
    move_start = (1, 4)  # For example, moving the white king's pawn from (1, 4) to (3, 4)
    move_end = (3, 4)

    result = chess_game.is_valid_move(move_start, move_end)
    print(result)
