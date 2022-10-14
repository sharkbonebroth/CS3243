from __future__ import annotations
import sys
from typing import Iterable, Tuple
from copy import deepcopy
import random

Position = Tuple[int, int] # row, col

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################

def is_within_grid(position: Position, board: Board) -> bool:
    return not (position[0] < 0 or position[0] >= board.row_max or position[1] < 0 or position[1] >= board.col_max)

def has_obstacle(position: Position, board: Board) -> bool:
    return (board.obstacle_grid[position[0]][position[1]] == -1)

def can_move_to(position: Position, board: Board) -> bool:
    return (is_within_grid(position, board) and not has_obstacle(position, board))

def get_projected_moves(position: Position, board: Board, direction_x: int, direction_y: int) -> Iterable[Position]:
    valid_moves = []
    i = 1
    while True:
        potential_goal_position = ((position[0] + i*direction_y), (position[1] + i*direction_x))
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
            i += 1
        else:
            break
    return valid_moves

class Piece:
    def __init__(
        self,
    ):
        self.num_pieces_threatening = 0

    def generate_threatened(self, position: Position, board: Board) -> Iterable[Position]:
        pass

class Ferz(Piece):
    def __str__(self) -> str:
        return "Ferz"

    def generate_threatened(self, position: Position, board: Board) -> Iterable[Position]:
        threatened = []
        potential_goal_position = (position[0] + 1, position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        self.threatened = threatened
        return threatened

class King(Ferz):
    def __str__(self) -> str:
        return "King"

    def generate_threatened(self, position: Position, board: Board) -> Iterable[Position]:
        threatened = super().generate_threatened(position, board)
        potential_goal_position = (position[0], position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0], position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1])
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1])
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        self.threatened = threatened
        return threatened

class Rook(Piece):
    def __str__(self) -> str:
        return "Rook"
        
    def generate_threatened(self, position: Position, board: Board) -> Iterable[Position]:
        threatened = []
        threatened += get_projected_moves(position, board, 1, 0)
        threatened += get_projected_moves(position, board, 0, 1)
        threatened += get_projected_moves(position, board, -1, 0)
        threatened += get_projected_moves(position, board, 0, -1)
        self.threatened = threatened
        return threatened

class Bishop(Piece):
    def __str__(self) -> str:
        return "Bishop"
        
    def generate_threatened(self, position: Position, board: Board) -> Iterable[Position]:
        threatened = []
        threatened += get_projected_moves(position, board, 1, 1)
        threatened += get_projected_moves(position, board, 1, -1)
        threatened += get_projected_moves(position, board, -1, 1)
        threatened += get_projected_moves(position, board, -1, -1)
        self.threatened = threatened
        return threatened

class Queen(Bishop):
    def __str__(self) -> str:
        return "Queen"
        
    def generate_threatened(self, position: Position, board: Board) -> Iterable[Position]:
        threatened = super().generate_threatened(position, board)
        threatened += get_projected_moves(position, board, 1, 0)
        threatened += get_projected_moves(position, board, 0, 1)
        threatened += get_projected_moves(position, board, -1, 0)
        threatened += get_projected_moves(position, board, 0, -1)
        self.threatened = threatened
        return threatened

class Knight(Piece):
    def __str__(self) -> str:
        return "Knight"
        
    def generate_threatened(self, position: Position, board: Board) -> Iterable[Position]:
        threatened = []
        potential_goal_position = (position[0] + 2, position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1] + 2)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] - 2, position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] + 2)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] + 2, position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1] - 2)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] - 2, position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] - 2)
        if (can_move_to(potential_goal_position, board)):
            threatened.append(potential_goal_position)
        self.threatened = threatened
        return threatened

class Princess(Knight):
    def __str__(self) -> str:
        return "Princess"
        
    def generate_threatened(self, position: Position, board: Board) -> Iterable[Position]:
        threatened = super().generate_threatened(position, board)
        threatened += get_projected_moves(position, board, 1, 1)
        threatened += get_projected_moves(position, board, 1, -1)
        threatened += get_projected_moves(position, board, -1, 1)
        threatened += get_projected_moves(position, board, -1, -1)
        self.threatened = threatened
        return threatened

class Empress(Knight):
    def __str__(self) -> str:
        return "Empress"
        
    def generate_threatened(self, position: Position, board: Board) -> Iterable[Position]:
        threatened = super().generate_threatened(position, board)
        threatened += get_projected_moves(position, board, 1, 0)
        threatened += get_projected_moves(position, board, 0, 1)
        threatened += get_projected_moves(position, board, -1, 0)
        threatened += get_projected_moves(position, board, 0, -1)
        self.threatened = threatened
        return threatened

#############################################################################
######## Board
#############################################################################

class Board:
    def __init__(
        self, 
        row_max: int,
        col_max: int,
        obstacle_grid: Iterable[Iterable[int]], # row by col array of int indicating whether there is an obstacle. -1 indicates that there is an obstacale
    ):
        self.row_max = row_max
        self.col_max = col_max
        self.obstacle_grid = obstacle_grid

#############################################################################
######## State
#############################################################################

class State:
    def __init__(
        self,
        board: Board,
        pieces: dict[Position, Piece],
        num_removed: int
    ):
        self.board = board
        self.pieces = pieces
        self.num_removed = num_removed

    def generate_moves(self) -> Iterable[Tuple[int, Position]]:
        moves = []
        for position, piece in self.pieces.items():
            cost_improvement = piece.num_pieces_threatening + len(piece.threatened)
            for threatened_position in piece.threatened:
                try:
                    self.pieces[threatened_position]
                except KeyError:
                    cost_improvement -= 1
            moves.append((cost_improvement, position))
        
        return moves

    def remove_piece(self, position: Position):
        for threatened_position in self.pieces[position].threatened:
            try:
                self.pieces[threatened_position].num_pieces_threatening -= 1
            except KeyError:
                pass
        try:
            self.pieces.pop(position)
        except:
            pass
            #print("trying to delete piece that does not exist on the board")
        self.num_removed += 1
            

    def is_terminal(self) -> bool:
        for _, piece in self.pieces.items():
            if piece.num_pieces_threatening != 0:
                return False
        return True
                

#############################################################################
######## Implement Search Algorithm
#############################################################################


class_dict = {
    "King": King,
    "Bishop": Bishop,
    "Knight": Knight,
    "Rook": Rook,
    "Queen": Queen,
    "Ferz": Ferz,
    "Princess": Princess,
    "Empress": Empress
}

def choose_move(moves: Iterable[Tuple[int, Position]]) -> Position:
    moves.sort(reverse = True)
    max_improvement = moves[0][0]
    valid_moves = [0]
    move_being_checked = 1
    while moves[move_being_checked][0] == max_improvement:
        valid_moves.append(move_being_checked)
        move_being_checked += 1
    
    return moves[random.choice(valid_moves)][1]

def format_for_answer(pieces: dict[Position, Piece]) -> dict[Tuple(str, int): str]:
    answer = {}
    for position, piece in pieces.items():
        answer[(chr(position[1] + 97), position[0])] = str(piece)

    return answer

def search(rows, cols, grid, pieces, k):
    board = Board(rows, cols, grid)
    pieces_classed = {}

    max_to_remove = len(pieces) - int(k)

    for position, piece_name in pieces.items():
        pieces_classed[position] = class_dict[piece_name]()
        pieces_classed[position].generate_threatened(position, board)

    for position, piece_classed in pieces_classed.items():
        threatened_new = []
        for threatened_position in piece_classed.threatened:
            try:
                pieces_classed[threatened_position].num_pieces_threatening += 1
                threatened_new.append(threatened_position)
            except KeyError:
                pass
        piece_classed.threatened = threatened_new

    initial_state = State(board, pieces_classed, 0)
    
    state = deepcopy(initial_state)

    while not state.is_terminal():
        if state.num_removed == max_to_remove:
            state = deepcopy(initial_state)
        moves = state.generate_moves()
        move = choose_move(moves)
        state.remove_piece(move)

    return format_for_answer(state.pieces)
        


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))
    cols = int(get_par(handle.readline()))
    grid = [[0 for j in range(cols)] for i in range(rows)]
    k = 0
    pieces = {}

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()
    
    k = handle.readline().split(":")[1].strip() # Read in value of k

    piece_nums = get_par(handle.readline()).split()
    num_pieces = 0
    for num in piece_nums:
        num_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        pieces[coords] = piece    

    return rows, cols, grid, pieces, k

def add_piece( comma_seperated):
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r,c), piece]

#Returns row and col index in integers respectively
def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces (String): King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, pieces, k = parse(testcase)
    goalstate = search(rows, cols, grid, pieces, k)
    return goalstate #Format to be returned

if __name__ == '__main__':
    run_local()