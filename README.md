# Sudoku-Game-GUI
A simple interactive sudoku game, solver and generator made using [pygame](https://github.com/pygame/pygame). Functions include:
- Interactive GUI with sudoku board, timer, mistake counter and an overview of all available controls
- Sketch function that allows up to four temporary values in each tile
- Tile selection control with arrow keys
- Sudoku generator using [dokusan](https://github.com/unmade/dokusan)
- A built-in solver with visualised solving steps using the backtracking algorithm
- Moral support cat

At the moment the average difficulty of newly generated sudokus is fixed at 100 in their ranking system. 

## Installation
Install requirements with `pip install -r requirements` and run the game with `python sudoku_gui.py`.


## Ideas for improvement
- Write own code for generating new sudokus
- Add a way to adjust generated sudoku difficulty

## Acknowledgement
This project was heavily inspired by https://github.com/techwithtim/Sudoku-GUI-Solver and the associated [YouTube video](https://www.youtube.com/watch?v=jl5yUEdekEM).
