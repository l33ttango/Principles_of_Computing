"""
Clone of 2048 game.
"""
# http://www.codeskulptor.org/#user40_IHKDm2dbZs_9.py

import poc_2048_gui
import simplegui
import random


# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.height
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def init_tiles(height, width):
    """
    Chooses one side of matrix as initial tiles according to direction
    """
    return {
        UP    : [(0, column) for column in range(width)],
        DOWN  : [(height - 1, column) for column in range(width)],
        RIGHT : [(row, width - 1) for row in range(height)],
        LEFT  : [(row, 0) for row in range(height)]}

    
def create_grid(height, width):
    """
    Create a grid of 0's 
    """    
    return [[0] * width for i in range(height)]

def add_vector(tile, offset):
    """
    Adds two vectors
    """
    height_coord = tile[0] + offset[0]
    width_coord = tile[1] + offset[1]
    return [height_coord, width_coord]

def move_tiles(matrix, first_tiles, height, width, offset):
    """ choosing one side of the matrix for work from, this uses  
    an offset to iterate over the entire matrix, pushing the 
    tiles in the direction chosen
    
    Takes 2 adjacent tiles with same value and merges them

    Takes a new grid of 0's and adds all new values to the grid
        """
    
    new_grid = create_grid(height, width)
    for each_tile in first_tiles:
        matrix_row = []
        
        current_tile = each_tile
        while is_valid_tile(current_tile, height, width):
            my_height, my_width = current_tile
            if matrix[my_height][my_width] != 0:
                matrix_row.append(matrix[my_height][my_width])
        
            current_tile = add_vector(current_tile, offset)
            
        length = len(matrix_row)
        

        squished_row = []
        while length >=2:            
            if matrix_row[0] == matrix_row[1]:
                squished_row.append(matrix_row.pop(0) + matrix_row.pop(0))
                length = len(matrix_row)
                
            else:
                squished_row.append(matrix_row.pop(0))
                length = len(matrix_row)
        squished_row += matrix_row
        
        if len(squished_row) > 0:
            current_tile = each_tile
            for row_item in squished_row:
                
                my_height, my_width = current_tile
                new_grid[my_height][my_width] = row_item
                current_tile = add_vector(current_tile, offset)

    matrix = new_grid
    return matrix
                
def is_valid_tile(pos, height, width):
    """
    Checks to see if pos is in matrix
    """
    my_height, my_width = pos
    return 0 <= my_height < height and 0 <= my_width < width

def seq_in_seq(subseq, seq):
    """
    checks to see if a subsequence is in a sequence, specifically, 2048
    """
    while subseq[0] in seq:
        index = seq.index(subseq[0])
        if subseq == seq[index:index + len(subseq)]:
            return True
        else:
            seq = seq[index + 1:]
    else:
        return False

def is_game_won(grid):
    """
    Checks to see if we won the game
    """
    for row in grid:
        if seq_in_seq([2, 0, 4, 8], row):
           return True
    return False
    
class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):

        self.grid_height = grid_height
        self.grid_width = grid_width
        
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.grid = create_grid(self.grid_height, self.grid_width)
        self.new_tile()
        self.new_tile()
                        

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        return str(self.grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """

        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """

        return self.grid_width
    
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        offset = OFFSETS[direction]
        
        first_tile_dict = init_tiles(self.grid_height, self.grid_width)
        first_tiles = first_tile_dict[direction]
        old_grid = self.grid
        self.grid = move_tiles(self.grid, first_tiles, self.grid_height, self.grid_width, offset)
        
        if is_game_won(self.grid):
            print "Yay"
        if self.grid != old_grid:
            self.new_tile()
        if is_game_won(self.grid):
            print "Yay!"
            
            # add more
            
    def new_tile(self):
        """TwentyFortyEight
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time. """
        new_grid = []
        for row in range(self.get_grid_height()):
            new_grid.append([])
        
        possible_tile_value = [2] * 9 + [4]
        new_row = random.randrange(self.grid_height)
        new_column = random.randrange(self.grid_width)
        new_tile_value = random.choice(possible_tile_value)
        
        for row in range(self.grid_height):
            for column in range(self.grid_width):
                if row != new_row or column != new_column:
                    new_grid[row].append(self.grid[row][column])
                elif self.grid[row][column] != 0:
                    return self.new_tile()
                else:
                    new_grid[row].append(new_tile_value)
                    
        
        self.grid = new_grid
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]                
        



poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

