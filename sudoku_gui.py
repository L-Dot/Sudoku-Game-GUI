import pygame
import time
from dokusan import generators
import numpy as np

pygame.init()

WHITE   = (255,255,255)
BLACK   = (0,0,0)
RED     = (204, 0, 0)
GREEN   = (0, 153, 0)
GRAY    = (96,96,96)
BLUE    = (0,64,255)

class Tile:
    """Object that represents a single tile in the Sudoku grid"""

    def __init__(self, value, row, col, gap):
        self.value = value
        self.row = row
        self.col = col
        self.gap = gap
        self.temp_values = []
        self.selected = False
        self.x = self.row*self.gap
        self.y = self.col*self.gap
        self.tile_rect = pygame.Rect(self.x+1, self.y+1, self.gap, self.gap)

    def add_temp(self, value):
        """Adds a temporary value to the tile"""
        if value not in self.temp_values and len(self.temp_values) < 4:
            self.temp_values = self.temp_values + [value]
        else:
            if value not in self.temp_values:
                self.temp_values[-1] = value

    def remove_temp(self):
        """Removes the last value in the temporary value list"""
        self.temp_values.pop(-1)

    def clear_temp(self):
        """Clears the tile of temporary values"""
        self.temp_values = []

    def set_val(self, value):
        """Sets the value of the tile"""
        self.value = value

    def draw(self, window, select_color=BLUE):
        """Draws the tile and the corresponding value within it"""

        # Draws temporary values
        if self.value == 0 and len(self.temp_values) != 0:
            xpos, ypos = self.tile_rect.topleft

            X = 0
            for tempval in self.temp_values:
                metric = tinyfont.metrics(str(tempval))
                text = tinyfont.render(str(tempval), True, GRAY)

                # Only highlight the value that is currently selected
                if tempval != key or not self.selected:
                    text.set_alpha(127)
 
                text_rect = text.get_rect(center = (xpos + X + 13, ypos + 18))
                window.blit(text, text_rect) 

                X += metric[0][-1]

        # Draw the set value
        elif self.value != 0:
            text = font.render(str(self.value), True, BLACK)
            text_rect = text.get_rect(center = self.tile_rect.center)
            window.blit(text, text_rect)

        # Draw the indicator if selected
        if self.selected:
            pygame.draw.rect(window, select_color, self.tile_rect, 3)

    def draw_solvestep(self, window, color=GREEN):
        """Draw function for the GUI solver"""

        pygame.draw.rect(window, WHITE, (self.x+1, self.y+1, self.gap, self.gap), 0)

        text = font.render(str(self.value), True, BLACK)
        text_rect = text.get_rect(center = self.tile_rect.center)
        window.blit(text, text_rect)
        pygame.draw.rect(window, color, (self.x+1, self.y+1, self.gap, self.gap), 3)


class Board:
    """Object representing the Sudoku board"""
    
    def __init__(self, window, board, nrows, ncols, boardWidth, boardHeight):
        self.nrows = nrows                  # number of rows on board
        self.ncols = ncols                  # number of cols on board
        self.win = window
        self.board = board
        self.model = None                   # model that stores the tile values
        self.boardWidth = boardWidth        # board width in pixels
        self.boardHeight = boardHeight      # board height in pixels
        self.gap = self.boardWidth / 9      # distance between gridlines
        self.selected = None                # currently selected row and col
        self.select_color = BLUE

        # Creating an array of tiles
        self.tiles = [[Tile(self.board[m][n], m, n, self.gap) for m in range(self.nrows)] for n in range(self.ncols)]
        
        self.update_model()

    def update_model(self):
        """Updating a model grid with values from the tiles"""
        self.model = [[self.tiles[m][n].value for n in range(self.ncols)] for m in range(self.nrows)]

    def draw(self):
        """Draws the initial board consisting of all the gridlines, 
        tiles and initial values"""

        # Draw all the gridlines
        for i in range(self.ncols + 1):
            if i % 3 == 0 and i != 0 and i != 9:
                linewidth = 5
            else:
                linewidth = 2
            pygame.draw.line(self.win, BLACK, (0, i*self.gap), (self.boardWidth, i*self.gap), linewidth)
            pygame.draw.line(self.win, BLACK, (i*self.gap, 0), (i*self.gap, self.boardHeight), linewidth)
                
        # Draw the tiles and their values
        for tile in [i for row in self.tiles for i in row]:
            tile.draw(self.win, self.select_color)

    def set_selected(self, row, col):
        """Updates the selected status of the selected tile and 
        stores information of which row and column is selected"""

        # Reset all tiles to not selected
        for m in range(self.nrows):
            for n in range(self.ncols):
                self.tiles[m][n].selected = False

        self.selected = (row, col)
        self.tiles[row][col].selected = True

    def reset_selected(self):
        """Resets the selection of tiles to nothing selected"""

        # Reset all tiles to not selected
        for m in range(self.nrows):
            for n in range(self.ncols):
                self.tiles[m][n].selected = False
        
        self.selected = None

    def move_selection(self, direction):
        """Moves the selection box by input of a given arrow direction"""
        row, col = self.selected
        self.tiles[row][col].selected = False

        if direction == 'UP':
            self.selected = ((row-1) % 9, col)
            self.tiles[(row-1) % 9][col].selected = True
        elif direction == 'DOWN':
            self.selected = ((row+1) % 9, col)
            self.tiles[(row+1) % 9][col].selected = True
        elif direction == 'LEFT':
            self.selected = (row, (col-1) % 9)
            self.tiles[row][(col-1) % 9].selected = True
        elif direction == 'RIGHT':
            self.selected = (row, (col+1) % 9)
            self.tiles[row][(col+1) % 9].selected = True

    def click_to_rowcol(self, pos):
        """Takes the x, y position of the click and returns a row and column value"""
        x, y = pos

        if x < self.boardWidth and y < self.boardHeight:
            row = int(y // self.gap)
            col = int(x // self.gap)
            return (row, col)
        else:
            return None

    def place_value(self, value):
        """Checks if the given value is valid in the current tile and draws if true"""
        row, col = self.selected
        if self.tiles[row][col].value == 0:
            self.tiles[row][col].set_val(value)
            self.update_model()

            if valid_check(self.model, row, col, value) and self.solve():
                return True
            else:
                self.tiles[row][col].set_val(0)
                self.update_model()
                return False

    def solve(self):
        """Solves the sudoku that is saved as the model by filling it in"""

        # Find the next empty tile
        next = next_empty(self.model)
        if not next:
            return True
        else:
            row, col = next

        # Backtracking algorithm
        for val in range(1, 10):
            if valid_check(self.model, row, col, val):
                self.model[row][col] = val

                # Check if model is complete
                if self.solve():
                    return True

                self.model[row][col] = 0
        return False

    def solve_in_gui(self):
        """Solves the Sudoku in the GUI"""

        self.update_model()
        next = next_empty(self.model)
        if not next:
            return True
        else:
            row, col = next

        # Backtracking algorithm with lines for drawing the tested values
        for val in range(1, 10):
            if valid_check(self.model, row, col, val):
                self.model[row][col] = val
                self.tiles[row][col].set_val(val)
                self.tiles[row][col].draw_solvestep(self.win, GREEN)
                self.update_model()
                pygame.display.flip()
                pygame.time.delay(10)

                if self.solve_in_gui():
                    return True

                self.model[row][col] = 0
                self.tiles[row][col].set_val(0)
                self.update_model()
                self.tiles[row][col].draw_solvestep(self.win, RED)
                pygame.display.flip()
                pygame.time.delay(10)
        
        return False   

    def check_finish(self):
        """Simple check to see if all empty grid places are gone"""
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.tiles[i][j].value == 0:
                    return False
        return True

def next_empty(board):
    """Finds the next empty tile on the board"""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

def valid_check(board, row, col, value):
    """Checks if the filled in solution value at a given row and column is valid"""

    # Row check
    for n in range(len(board[0])):
        if board[row][n] == value and col != n:
            return False
        
    # Column check
    for m in range(len(board)):
        if board[m][col] == value and row != m:
            return False
    
    # Box check
    box_x = col // 3
    box_y = row // 3

    for m in range(box_y*3, box_y*3 + 3):
        for n in range(box_x * 3, box_x*3 + 3):
            if board[m][n] == value and (m,n) != (row,col):
                return False
    
    return True

def time_format(secs):
    """Convert time in seconds to nice format"""
    t = time.strftime("%M:%S", time.gmtime(secs))
    return t

def generate_sudoku(rank):
    """Generates a new 9x9 sudoku grid with a given rank"""
    new_list = np.array(list(str(generators.random_sudoku(avg_rank=rank))), dtype=int)
    new_grid = new_list.reshape(9,9)
    return new_grid

def draw_window(window, board, time, mistakes, finished):
    """Draws the window and everything displayed on it"""
    window.fill(WHITE)

    # Draw the time box
    timebox = pygame.Rect(720, 0, 270, 162)
    pygame.draw.rect(window, BLACK, timebox, 2)
    text = timefont.render(time_format(time), 1, BLACK)
    text_rect = text.get_rect(center = timebox.center)
    window.blit(text, text_rect)

    # Draw the mistake box
    errbox = pygame.Rect(720, 160, 270, 81)
    pygame.draw.rect(window, BLACK, errbox, 2)
    text = errfont.render(f"Mistakes:  {mistakes}", True, BLACK)
    text_rect = text.get_rect(center = errbox.center)
    window.blit(text, text_rect)

    # Draw instructions box
    commbox = pygame.Rect(720, 239, 270, 323)
    pygame.draw.rect(window, BLACK, commbox, 2)
    
    vbox1 = pygame.Rect(720, 239, 135, 280)
    t1 = commfont.render(f"LMB  = ", True, BLACK)
    t2 = commfont.render(f"↑↓→←  = ", True, BLACK)
    t3 = commfont.render(f"NUM  = ", True, BLACK)
    t4 = commfont.render(f"ENTER  = ", True, BLACK)
    t5 = commfont.render(f"DEL  = ", True, BLACK)
    t6 = commfont.render(f"R  = ", True, BLACK)
    t7 = commfont.render(f"SPACE  = ", True, BLACK)
    t8 = commfont.render(f"G  = ", True, BLACK)
    t9 = commfont.render(f"ESC  = ", True, BLACK)

    x1, y1 = vbox1.topright
    x1 += 20
    y1 += 3
    window.blit(t1, t1.get_rect(topright=(x1, y1)))
    window.blit(t2, t2.get_rect(topright=(x1, y1+35)))
    window.blit(t3, t3.get_rect(topright=(x1, y1+70)))
    window.blit(t4, t4.get_rect(topright=(x1, y1+105)))
    window.blit(t5, t5.get_rect(topright=(x1, y1+140)))
    window.blit(t6, t6.get_rect(topright=(x1, y1+175)))
    window.blit(t7, t7.get_rect(topright=(x1, y1+210)))
    window.blit(t8, t8.get_rect(topright=(x1, y1+245)))
    window.blit(t9, t9.get_rect(topright=(x1, y1+280)))

    vbox2 = pygame.Rect(855, 239, 135, 402)
    p1 = commfont.render(f"select", True, BLACK)
    p2 = commfont.render(f"select", True, BLACK)
    p3 = commfont.render(f"sketch", True, BLACK)
    p4 = commfont.render(f"guess", True, BLACK)
    p5 = commfont.render(f"clear", True, BLACK)
    p6 = commfont.render(f"restart", True, BLACK)
    p7 = commfont.render(f"solve", True, BLACK)
    p8 = commfont.render(f"new", True, BLACK)
    p9 = commfont.render(f"quit", True, BLACK)
   
    x2, y2 = vbox2.topleft
    x2 += 30
    y2 += 3
    window.blit(p1, p1.get_rect(topleft=(x2, y2)))
    window.blit(p2, p2.get_rect(topleft=(x2, y2+35)))
    window.blit(p3, p3.get_rect(topleft=(x2, y2+70)))
    window.blit(p4, p4.get_rect(topleft=(x2, y2+105)))
    window.blit(p5, p5.get_rect(topleft=(x2, y2+140)))
    window.blit(p6, p6.get_rect(topleft=(x2, y2+175)))
    window.blit(p7, p7.get_rect(topleft=(x2, y2+210)))
    window.blit(p8, p8.get_rect(topleft=(x2, y2+245)))
    window.blit(p9, p9.get_rect(topleft=(x2, y2+280)))

    # Draw end screen
    if finished:
        endbox = pygame.Rect(990/4, 270, 500,150)
        text = endfont.render("Well done!", True, BLACK)
        text_rect = text.get_rect(center = endbox.center)
        window.blit(text, text_rect)

    # Draw cat box
    catbox = pygame.Rect(720, 560, 270, 162)
    pygame.draw.rect(window, BLACK, catbox, 2)
    catImg = pygame.image.load('moral_support_cat.png')
    window.blit(catImg, catbox.topleft)

    # Draw the board
    board.draw()

def main():
    """Function that initialises the game"""
    wWidth  = 990
    wHeight = 721
    bWidth  = 720
    bHeight = 720
    nrow = ncol = 9

    # Initializing the window, board and starting parameters
    win = pygame.display.set_mode((wWidth, wHeight))
    pygame.display.set_caption("Sudokupy")
    board = Board(win, init_board, nrow, ncol, bWidth, bHeight)

    start   = time.time()
    mistakes  = 0
    finished = False
    global key
    key = None

    running = True
    while running:

        total_time = time.time() - start

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                board.select_color = BLUE

                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                
                elif event.key == pygame.K_UP:
                    key = 'UP'
                elif event.key == pygame.K_DOWN:
                    key = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    key = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    key = 'RIGHT'           

                elif event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    board.solve_in_gui()

                    if board.check_finish():
                        end_time = total_time
                        finished = True

                elif event.key == pygame.K_r:
                    board = Board(win, board.board, nrow, ncol, bWidth, bHeight)
                    start   = time.time()
                    mistakes  = 0
                    finished = False
                    key = None
                
                elif event.key == pygame.K_g:
                    new_board = generate_sudoku(100)
                    board = Board(win, new_board, nrow, ncol, bWidth, bHeight)
                    start   = time.time()
                    mistakes  = 0
                    finished = False
                    key = None

                elif event.key == pygame.K_RETURN and board.selected and type(key) == int:
                    row, col = board.selected
                    
                    if board.place_value(key):
                        board.select_color = GREEN
                    else:
                        mistakes += 1
                        board.tiles[row][col].temp_values.remove(key)
                        board.select_color = RED
                    key = None

                    # Game ends
                    if board.check_finish():
                        end_time = total_time
                        finished = True
                
                # Adds a temporary value to the selected tile
                if board.selected and type(key) == int:
                    row, col = board.selected
                    board.tiles[row][col].add_temp(key)

                # Clears the selected tile of temporary values
                if board.selected and event.key == pygame.K_DELETE:
                    row, col = board.selected
                    board.tiles[row][col].clear_temp()
                    key = None

                # Removes the last value added to temporary values
                if board.selected and event.key == pygame.K_BACKSPACE:
                    row, col = board.selected
                    board.tiles[row][col].remove_temp()
                    key = None

                # Moves the selection border
                if key in {'UP', 'DOWN', 'LEFT', 'RIGHT'}:
                    if board.selected:
                        board.move_selection(key)
                        key = None
                    else:
                        board.selected = (4,4)
                        board.move_selection(key)
                        key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                board.select_color = BLUE

                # Left click
                if event.button == 1:
                    pos = event.pos
                    on_board = board.click_to_rowcol(pos)
                    
                    # Selects a tile if click was on the board
                    if on_board != None:
                        board.set_selected(*on_board)
                        key = None
                    else:
                        board.reset_selected()
                        key = None

        # Draw the window
        if not finished:
            draw_window(win, board, total_time, mistakes, finished)
        else:
            draw_window(win, board, end_time, mistakes, finished)

        pygame.display.flip()

# Some useful settings
font = pygame.font.SysFont('lato', 50)
tinyfont = pygame.font.SysFont('lato', 30)
errfont = pygame.font.SysFont('lato', 40)
timefont = pygame.font.SysFont('lato', 70)
commfont = pygame.font.SysFont('lato', 30)
endfont = pygame.font.SysFont('lato', 100)

# The initial board
init_board = [
    [0,1,0,0,3,0,9,0,2],
    [0,0,0,0,0,2,0,1,0],
    [0,6,2,7,0,8,5,0,0],
    [1,7,0,8,4,3,6,2,9],
    [0,4,3,6,0,0,1,7,0],
    [0,2,9,0,0,5,8,0,3],
    [3,8,0,0,0,1,0,9,0],
    [0,0,0,2,0,0,3,8,7],
    [2,9,0,3,8,0,4,5,0]
]

if __name__ == '__main__':
    main()
    pygame.quit()