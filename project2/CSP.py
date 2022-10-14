from __future__ import annotations
import sys
from typing import Iterable, Tuple
from copy import deepcopy

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
        obstacle_grid: Iterable[Iterable[int]], # row by col array of int indicating whether there is an obstacle. -1 indicates that there is an obstacale.
        threatened_grid: Iterable[Iterable[bool]], # row by col array of bool indicating whether a square is threatened.
        occupancy_grid: Iterable[Iterable[bool]], # row by col array of bool indicating whether a square has a piece there.
        num_unthreatened: int
    ):
        self.row_max = row_max
        self.col_max = col_max
        self.obstacle_grid = obstacle_grid
        self.threatened_grid = threatened_grid
        self.occupancy_grid = occupancy_grid
        self.num_unthreatened = num_unthreatened

    def new_board_from_assignment(self, assignment: Tuple[Position, Piece]) -> Board:
        new_threatened_grid = deepcopy(self.threatened_grid)
        new_num_unthreatened = self.num_unthreatened
        position_assigned = assignment[0]
        new_threatened_positions = assignment[1].generate_threatened(position_assigned, self)
        for Position in new_threatened_positions:
            if new_threatened_grid[Position[0]][Position[1]] == False:
                new_num_unthreatened -= 1
                new_threatened_grid[Position[0]][Position[1]] = True

        new_occupancy_grid = deepcopy(self.occupancy_grid)
        new_occupancy_grid[position_assigned[0]][position_assigned[1]] = True

        return Board(
            self.row_max,
            self.col_max,
            self.obstacle_grid,
            new_threatened_grid,
            new_occupancy_grid,
            new_num_unthreatened
        )


#############################################################################
######## State
#############################################################################
class State:
    pass

#############################################################################
######## Implement Search Algorithm
#############################################################################

unassigned_pieces_priority = [
    "Queen",
    "Princess",
    "Empress",
    "Bishop",
    "Rook",
    "Knight",
    "King", 
    "Ferz"
]

# Based on what is given in test cases
parsed_order = {
    "King": 0,
    "Queen": 1,
    "Bishop": 2,
    "Rook": 3,
    "Knight": 4,
    "Ferz": 5,
    "Princess": 6,
    "Empress": 7
}

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
    
def get_piece_to_assign(unassigned_pieces: Iterable[int]) -> Piece:
    for piece_type in unassigned_pieces_priority:
        if unassigned_pieces[parsed_order[piece_type]] != 0:
            return class_dict[piece_type]()

def get_domain_value_order(piece: Piece, board: Board) -> Iterable[Position]:
    valid_position_assignments = []
    for row in range(len(board.threatened_grid)):
        for col in range(len(board.threatened_grid[row])):
            if not board.threatened_grid[row][col] and not board.occupancy_grid[row][col] and not board.obstacle_grid[row][col] == -1:
                new_threatened_positions = piece.generate_threatened((row, col), board)
                additional_grids_threatened = 0
                is_valid = True

                for new_threatened_position in new_threatened_positions:
                    if board.occupancy_grid[new_threatened_position[0]][new_threatened_position[1]]:
                        is_valid = False
                        break
                    if not board.threatened_grid[new_threatened_position[0]][new_threatened_position[1]]:
                        additional_grids_threatened += 1
                
                if is_valid:
                    valid_position_assignments.append((additional_grids_threatened, (row, col)))
    
    valid_position_assignments.sort()
    return [valid_position_assignment[1] for valid_position_assignment in valid_position_assignments]

def inference(unassigned_pieces: Iterable[int], board: Board):
    if sum(unassigned_pieces) > board.num_unthreatened:
        return False
    return True   

def format_for_answer(pieces: dict[Position, Piece]) -> dict[Tuple(str, int): str]:
    answer = {}
    for position, piece in pieces.items():
        answer[(chr(position[1] + 97), position[0])] = str(piece)
    return answer

def backtrack(unassigned_pieces: Iterable[int], board: Board, assignments: dict[Position, str]) -> dict[Position, str]:
    if (sum(unassigned_pieces) == 0):
        return assignments
    piece_to_assign = get_piece_to_assign(unassigned_pieces)
    for assignment in get_domain_value_order(piece_to_assign, board):
        unassigned_pieces[parsed_order[str(piece_to_assign)]] -= 1
        assignments[assignment] = str(piece_to_assign)
        new_board = board.new_board_from_assignment((assignment, piece_to_assign))
        if inference(unassigned_pieces, new_board):
            result = backtrack(unassigned_pieces, new_board, assignments)
            if result != False:
                return result
        assignments.pop(assignment)
        unassigned_pieces[parsed_order[str(piece_to_assign)]] += 1
    return False
        

def search(rows, cols, grid, num_pieces):
    initial_board_threatened_grid = [[False for j in range(cols)] for i in range(rows)]
    initial_board_occupancy_grid = [[False for j in range(cols)] for i in range(rows)]
    initial_num_unthreatened = rows * cols
    initial_board = Board(
        rows,
        cols,
        grid,
        initial_board_threatened_grid,
        initial_board_occupancy_grid,
        initial_num_unthreatened
    )
    assignments = backtrack(num_pieces, initial_board, {})
    return format_for_answer(assignments)
    

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

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()
    
    piece_nums = get_par(handle.readline()).split()
    num_pieces = [int(x) for x in piece_nums] #List in the order of King, Queen, Bishop, Rook, Knight

    return rows, cols, grid, num_pieces

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
def run_CSP():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, num_pieces = parse(testcase)
    goalstate = search(rows, cols, grid, num_pieces)
    return goalstate #Format to be returned

if __name__ == '__main__':
    run_CSP()