# Chess Recognition and Game Application

This application combines chessboard recognition and chess game logic to create an online board with live moves. It is designed to work with a live feed or images of a chessboard. The application detects moves, updates the game state, and provides a graphical representation of the chessboard.

## Table of Contents
- [File Structure](#file-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Important Notes](#important-notes)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## File Structure

- `main_game.py`: Contains the main game logic, serving as the controller that orchestrates different components.
- `chess_logic.py`: Implements the core chess game logic, including move validation and game state management.
- `chess_app_graphics.py`: Manages the graphical aspects of the application, such as displaying the chessboard and pieces.
- `chess_recognition.py`: Handles chessboard recognition, piece movement detection, and related functionalities.
- `img/`: Folder containing images of chess pieces and the chessboard.

A `games/` folder is automatically generated to store game data, and an empty chessboard image (`chessboardEmpty.jpg`) is stored in the main folder.

## Installation

Ensure you have Python installed. Run the following commands to set up the required libraries:

```bash
pip install opencv-python pillow scikit-image
```

## Usage

1. Adjust the URL at the bottom of the `main_game.py` to match the location where you stream the live chessboard.
2. Run the main loop in `main_game.py`.

## Important Notes

- The application requires a clear and unobstructed view of the chessboard. Ensure the board is well-visible in pictures taken from the top.
- Only press the spacebar or click the clock when the board is not obstructed.
- Pawn promotion is not yet implemented!

## Features

- Live chessboard recognition.
- Automatic generation of a `games/` folder for storing game data.
- Detection of legal moves, including castling, en passant, and double pawn moves.
- Graphical representation of the chessboard during gameplay.

## Contributing

Feel free to contribute by opening issues or submitting pull requests.
