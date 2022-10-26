from __future__ import annotations
import sys
from typing import Iterable, Tuple
from copy import deepcopy
import time

Position = Tuple[int, int] # row, col

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
def is_within_grid(position: Position, board: Board) -> bool:
    return not (position[0] < 0 or position[0] >= board.row_max or position[1] < 0 or position[1] >= board.col_max)

def is_occupied_by_friendly_piece(position: Position, board: Board, allignment: int) -> bool:
    if board.piece_grid[position[0]][position[1]] == None:
        return False
    if allignment == board.piece_grid[position[0]][position[1]].allignment:
        return True
    return False

def is_occupied_by_enemy_piece(position: Position, board: Board, allignment: int) -> bool:
    if board.piece_grid[position[0]][position[1]] == None:
        return False
    if allignment == -board.piece_grid[position[0]][position[1]].allignment:
        return True
    return False

def can_move_to(position: Position, board: Board, allignment: int) -> bool:
    return (is_within_grid(position, board) and not is_occupied_by_friendly_piece(position, board, allignment))

def get_projected_moves(position: Position, board: Board, direction_x: int, direction_y: int, allignment: int) -> Iterable[Position]:
    valid_moves = []
    i = 1
    while True:
        potential_goal_position = ((position[0] + i*direction_y), (position[1] + i*direction_x))
        if (can_move_to(potential_goal_position, board, allignment)):
            valid_moves.append(potential_goal_position)
            i += 1
        if (is_occupied_by_enemy_piece(position, board, allignment)):
            break
        else:
            break
    return valid_moves

class Piece:
    piece_value = None

    def __init__(
        self,
        allignment: int # White = 1 | Black = -1
    ):
        self.allignment = allignment

    def get_moves(
        self,
        position: Position,
        board: Board
    ) -> Iterable[Position]:
        pass

class Pawn(Piece):
    piece_value = 100

    def __str__(self) -> str:
        return "Pawn"

    def get_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = []
        potential_goal_position = (position[0] + self.allignment, position[1])
        if (can_move_to(potential_goal_position, board, self.allignment) and not is_occupied_by_enemy_piece(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)

        # For captures
        potential_goal_position = (position[0] + self.allignment, position[1] + 1)
        if (can_move_to(potential_goal_position, board, self.allignment) and is_occupied_by_enemy_piece(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + self.allignment, position[1] - 1)
        if (can_move_to(potential_goal_position, board, self.allignment) and is_occupied_by_enemy_piece(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        return valid_moves
        
class Ferz(Piece):
    piece_value = 200

    def __str__(self) -> str:
        return "Ferz"

    def get_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = []
        potential_goal_position = (position[0] + 1, position[1] + 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] + 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1] - 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] - 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        return valid_moves

class King(Ferz):
    piece_value = 50000

    def __str__(self) -> str:
        return "King"

    def get_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = super().get_moves(position, board)
        potential_goal_position = (position[0], position[1] + 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0], position[1] - 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1])
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1])
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        return valid_moves

class Rook(Piece):
    piece_value = 500

    def __str__(self) -> str:
        return "Rook"
        
    def get_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = []
        valid_moves += get_projected_moves(position, board, 1, 0, self.allignment)
        valid_moves += get_projected_moves(position, board, 0, 1, self.allignment)
        valid_moves += get_projected_moves(position, board, -1, 0, self.allignment)
        valid_moves += get_projected_moves(position, board, 0, -1, self.allignment)
        return valid_moves

class Bishop(Piece):
    piece_value = 330

    def __str__(self) -> str:
        return "Bishop"
        
    def get_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = []
        valid_moves += get_projected_moves(position, board, 1, 1, self.allignment)
        valid_moves += get_projected_moves(position, board, 1, -1, self.allignment)
        valid_moves += get_projected_moves(position, board, -1, 1, self.allignment)
        valid_moves += get_projected_moves(position, board, -1, -1, self.allignment)
        return valid_moves

class Queen(Bishop):
    piece_value = 900

    def __str__(self) -> str:
        return "Queen"
        
    def get_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = super().get_moves(position, board)
        valid_moves += get_projected_moves(position, board, 1, 0, self.allignment)
        valid_moves += get_projected_moves(position, board, 0, 1, self.allignment)
        valid_moves += get_projected_moves(position, board, -1, 0, self.allignment)
        valid_moves += get_projected_moves(position, board, 0, -1, self.allignment)
        return valid_moves

class Knight(Piece):
    piece_value = 320

    def __str__(self) -> str:
        return "Knight"
        
    def get_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = []
        potential_goal_position = (position[0] + 2, position[1] + 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1] + 2)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 2, position[1] + 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] + 2)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 2, position[1] - 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1] - 2)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 2, position[1] - 1)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] - 2)
        if (can_move_to(potential_goal_position, board, self.allignment)):
            valid_moves.append(potential_goal_position)
        return valid_moves

class Princess(Knight):
    piece_value = 650

    def __str__(self) -> str:
        return "Princess"
        
    def get_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = super().get_moves(position, board)
        valid_moves += get_projected_moves(position, board, 1, 1, self.allignment)
        valid_moves += get_projected_moves(position, board, 1, -1, self.allignment)
        valid_moves += get_projected_moves(position, board, -1, 1, self.allignment)
        valid_moves += get_projected_moves(position, board, -1, -1, self.allignment)
        return valid_moves

class Empress(Knight):
    piece_value = 820

    def __str__(self) -> str:
        return "Empress"
        
    def get_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = super().get_moves(position, board)
        valid_moves += get_projected_moves(position, board, 1, 0, self.allignment)
        valid_moves += get_projected_moves(position, board, 0, 1, self.allignment)
        valid_moves += get_projected_moves(position, board, -1, 0, self.allignment)
        valid_moves += get_projected_moves(position, board, 0, -1, self.allignment)
        return valid_moves

#############################################################################
######## Board
#############################################################################
class Board:
    def __init__(
        self,
        row_max: int,
        col_max: int,
        piece_grid: Iterable[Iterable[Piece]] # row by col array of pieces indicating the board state
    ):
        self.row_max = row_max
        self.col_max = col_max
        self.piece_grid = piece_grid

    def get_all_valid_moves(self, allignment: int) -> Iterable[(Tuple[Position, Position])]:
        all_valid_moves = []
        for row in range(self.col_max):
            for col in range(self.row_max):
                if self.piece_grid[row][col] is not None:
                    if self.piece_grid[row][col].allignment == allignment:
                        valid_moves = self.piece_grid[row][col].get_moves((row, col), self)
                        all_valid_moves += [((row, col), valid_move) for valid_move in valid_moves]

        return all_valid_moves

    def move(self, position_of_piece: Position, destination: Position) -> Board:
        new_board = deepcopy(self)
        new_board.piece_grid[destination[0]][destination[1]] = new_board.piece_grid[position_of_piece[0]][position_of_piece[1]] 
        new_board.piece_grid[position_of_piece[0]][position_of_piece[1]]  = None
        return new_board

#############################################################################
######## State
#############################################################################
class State:
    def __init__(
        self,
        board: Board,
        move_to_achieve: Tuple[Position, Position],
        ab_alignment: int # White = 1 | Black = -1
    ):
        self.board = board
        self.move_to_achieve = move_to_achieve
        self.ab_alignment = ab_alignment

        self.all_valid_moves = self.board.get_all_valid_moves(self.ab_alignment)
        self.valid_move_index = 0
        self.num_child_states = len(self.all_valid_moves)

    def evaluate_heuristics(self) -> int:
        score = 0
        for row in self.board.piece_grid:
            for piece in row:
                if piece is not None:
                    score += piece.piece_value * piece.allignment
        
        return score

    def is_terminal(self) -> int: # -1: is_terminal for min agent. 1: is_terminal for max agent, 0: not is_terminal
        return (self.evaluate_heuristics() < -35000 or self.evaluate_heuristics() > 35000)

    def get_all_child_states(self) -> Iterable[State]:
        all_child_states = [State(self.board.move(move[0], move[1]), move, -self.ab_alignment) for move in self.all_valid_moves]

        return all_child_states

    def get_next_child_state(self) -> State:
        if (self.valid_move_index == self.num_child_states):
            return None
        else:
            move = self.all_valid_moves[self.valid_move_index]
            self.valid_move_index += 1
            return State(self.board.move(move[0], move[1]), move, -self.ab_alignment)

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(
    state: State, 
    depth: int, 
    max_depth: int, 
    is_maximising: bool,
    alpha: int,
    beta: int
) -> Tuple[Tuple[Position, Position], int]: # (move_to_achieve, score)
    if max_depth == depth:
        return (None, state.evaluate_heuristics())
    
    if (is_maximising):
        best_value = float('-inf')
        best_child_state = None
        child_state = state.get_next_child_state()
        while child_state is not None:
            if child_state.is_terminal():
                return (child_state.move_to_achieve, float('inf'))

            value = ab(
                state = child_state,
                depth = depth + 1,
                max_depth = max_depth,
                is_maximising = False,
                alpha = alpha,
                beta = beta
            )[1]

            if value > best_value:
                best_value = value
                best_child_state = child_state

                if best_value > alpha:
                    #print(f"alpha updated! new val: {best_value} prev val: {alpha}")
                    alpha = best_value
            
            if beta <= alpha:
                break

            child_state = state.get_next_child_state()

        return (best_child_state.move_to_achieve, best_value)

    else:
        best_value = float('inf')
        best_child_state = None
        child_state = state.get_next_child_state()
        while child_state is not None:
            if child_state.is_terminal():
                return (child_state.move_to_achieve, float('-inf'))

            value = ab(
                state = child_state,
                depth = depth + 1,
                max_depth = max_depth,
                is_maximising = True,
                alpha = alpha,
                beta = beta
            )[1]

            if value < best_value:
                best_value = value
                best_child_state = child_state

                if best_value < beta:
                    #print(f"beta updated! new val: {best_value} prev val: {beta}")
                    beta = best_value

            if alpha >= beta:
                break

            child_state = state.get_next_child_state()

        return (best_child_state.move_to_achieve, best_value)

            

    

#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# Return number of rows, cols, grid containing obstacles and step costs of coordinates, enemy pieces, own piece, and goal positions
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline())) # Integer
    cols = int(get_par(handle.readline())) # Integer
    gameboard = {}
    
    enemy_piece_nums = get_par(handle.readline()).split()
    num_enemy_pieces = 0 # Read Enemy Pieces Positions
    for num in enemy_piece_nums:
        num_enemy_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_enemy_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "Black")    

    own_piece_nums = get_par(handle.readline()).split()
    num_own_pieces = 0 # Read Own Pieces Positions
    for num in own_piece_nums:
        num_own_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_own_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "White")    

    return rows, cols, gameboard

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    c = ch_coord[0]
    r = int(ch_coord[1])
    return [(c, r), piece]

def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

# You may call this function if you need to set up the board
def setUpBoard():
    config = sys.argv[1]
    rows, cols, gameboard = parse(config)
    return gameboard

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook, Princess, Empress, Ferz, Pawn (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new ending position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def format_for_answer(move: Tuple[Position, Position]) -> Tuple[Tuple[str, int], Tuple[str, int]]:
    initial_pos = move[0]
    final_pos = move[1]
    return ((chr(initial_pos[1] + 97), initial_pos[0]), (chr(final_pos[1] + 97), final_pos[0]))

class_dict = {
    "King": King,
    "Bishop": Bishop,
    "Knight": Knight,
    "Rook": Rook,
    "Queen": Queen,
    "Ferz": Ferz,
    "Pawn": Pawn,
    "Princess": Princess,
    "Empress": Empress
}

allignment_dict = {
    "White": 1,
    "Black": -1,
}
from_chess_coord
def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type

    piece_grid = [[None for i in range(7)] for j in range(7)]
    for position, piece in gameboard.items():
        position = (int(position[1]), ord(position[0]) - 97)
        piece_grid[position[0]][position[1]] = class_dict[piece[0]](allignment_dict[piece[1]])

    curr_board_state =  Board(
        row_max = 7,
        col_max = 7,
        piece_grid = piece_grid
    )

    curr_game_state = State(
        board = curr_board_state,
        move_to_achieve = None,
        ab_alignment= 1
    )

    move, best_score = ab(
        state = curr_game_state,
        depth = 0,
        max_depth = 2,
        is_maximising = True,
        alpha = float('-inf'),
        beta = float('inf')
    )

    return format_for_answer(move) #Format to be returned (('a', 0), ('b', 3))

if __name__ == "__main__":
    gameboard = setUpBoard()
    start_time = time.time()
    move = studentAgent(gameboard)
    end_time = time.time()