from __future__ import annotations
import sys
from typing import Iterable, Tuple, Callable
from collections import deque
from queue import PriorityQueue

Position = Tuple[int, int] # row, col
Move = Iterable[Position] # position tuple, next position tuple

class Board:
    def __init__(
        self, 
        row_max: int, # holds the maximum number of rows
        col_max: int, # holds the maximum number of columns
        occupancy_grid: Iterable[Iterable[bool]], # Array of arrays containing where pieces are at. We are going to hack this grid to double as the movability_grid for the king
        ):

        self.row_max = row_max
        self.col_max = col_max
        self.occupancy_grid = occupancy_grid


#############################################################################
######## Piece
#############################################################################

def is_within_grid(position: Position, board: Board) -> bool:
    return not (position[0] < 0 or position[0] >= board.row_max or position[1] < 0 or position[1] >= board.col_max)

def is_occupied(position: Position, board: Board) -> bool:
    return (board.occupancy_grid[position[0]][position[1]])

def can_move_to(position: Position, board: Board) -> bool:
    return (is_within_grid(position, board) and not is_occupied(position, board))

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
    def __init__(self):
        pass

    def generate_moves(self, position: Position, board: Board) -> Iterable[Position]:
        # Generate moves for the piece based on its position, returns a list of next positions
        pass

class Ferz(Piece):
    def generate_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = []
        potential_goal_position = (position[0] + 1, position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        return valid_moves

class King(Ferz):
    def generate_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = super().generate_moves(position, board)
        potential_goal_position = (position[0], position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0], position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1])
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1])
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        return valid_moves

class Rook(Piece):
    def generate_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = []
        valid_moves += get_projected_moves(position, board, 1, 0)
        valid_moves += get_projected_moves(position, board, 0, 1)
        valid_moves += get_projected_moves(position, board, -1, 0)
        valid_moves += get_projected_moves(position, board, 0, -1)
        return valid_moves

class Bishop(Piece):
    def generate_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = []
        valid_moves += get_projected_moves(position, board, 1, 1)
        valid_moves += get_projected_moves(position, board, 1, -1)
        valid_moves += get_projected_moves(position, board, -1, 1)
        valid_moves += get_projected_moves(position, board, -1, -1)
        return valid_moves

class Queen(Bishop):
    def generate_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = super().generate_moves(position, board)
        valid_moves += get_projected_moves(position, board, 1, 0)
        valid_moves += get_projected_moves(position, board, 0, 1)
        valid_moves += get_projected_moves(position, board, -1, 0)
        valid_moves += get_projected_moves(position, board, 0, -1)
        return valid_moves

class Knight(Piece):
    def generate_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = []
        potential_goal_position = (position[0] + 2, position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1] + 2)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 2, position[1] + 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] + 2)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 2, position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] + 1, position[1] - 2)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 2, position[1] - 1)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        potential_goal_position = (position[0] - 1, position[1] - 2)
        if (can_move_to(potential_goal_position, board)):
            valid_moves.append(potential_goal_position)
        return valid_moves

class Princess(Knight):
    def generate_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = super().generate_moves(position, board)
        valid_moves += get_projected_moves(position, board, 1, 1)
        valid_moves += get_projected_moves(position, board, 1, -1)
        valid_moves += get_projected_moves(position, board, -1, 1)
        valid_moves += get_projected_moves(position, board, -1, -1)
        return valid_moves

class Empress(Knight):
    def generate_moves(self, position: Position, board: Board) -> Iterable[Position]:
        valid_moves = super().generate_moves(position, board)
        valid_moves += get_projected_moves(position, board, 1, 0)
        valid_moves += get_projected_moves(position, board, 0, 1)
        valid_moves += get_projected_moves(position, board, -1, 0)
        valid_moves += get_projected_moves(position, board, 0, -1)
        return valid_moves

#############################################################################
######## State
#############################################################################

class State:
    def __init__(
        self,
        king_position: Position, 
        board: Board, 
        parent_state: State = None,
        ):

        self.king_position = king_position
        self.board = board
        self.parent_state = parent_state

#############################################################################
######## Frontiers
#############################################################################

class Frontier:
    def __init__():
        pass

    def push(self, state: State) -> None:
        pass

    def pop(self) -> State:
        pass

    def is_empty(self) -> bool:
        pass

class BFS_frontier(Frontier):
    def __init__(self):
        self.frontier = deque()

    def push(self, state: State) -> None:
        self.frontier.append(state)

    def pop(self) -> State:
        return self.frontier.popleft()

    def is_empty(self) -> bool:
        return not self.frontier

class DFS_frontier(BFS_frontier):
    def __init__(self):
        self.frontier = []

    def push(self, state: State) -> None:
        self.frontier.append(state)

    def pop(self) -> State:
        return self.frontier.pop()

    def is_empty(self) -> bool:
        return not self.frontier


#############################################################################
######## The SEARCHER
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


class Searcher:
    def __init__(
            self, 
            frontier: Frontier, 
            start_position: Position,
            row_max: int,
            col_max: int,
            enemy_pieces: Iterable[str, Position],
            goals: Iterable[Position,],
            grid: Iterable[Iterable[int]]
        ):

        self.frontier = frontier
        self.start_position = start_position
        self.row_max = row_max
        self.col_max = col_max
        self.enemy_pieces = enemy_pieces
        self.goals = goals
        self.grid = grid
        
        # populate the occupancy_grid with obstacles
        occupancy_grid = [[True if grid[j][i] == -1 else False for i in range(col_max)] for j in range(row_max)]

        # now populate it with enemy pieces
        for enemy, position in enemy_pieces:
            occupancy_grid[position[0]][position[1]] = True

        # populate the occupancy_grid with threatened positions
        board = Board(
            row_max,
            col_max,
            occupancy_grid,
        )

        # Create classes for each enemy piece to generate threatened squares
        enemy_pieces_classed = []
        for enemy_piece in enemy_pieces:
            enemy_pieces_classed.append((class_dict[enemy_piece[0]](), enemy_piece[1]))

        threatened_positions = []
        for enemy, position in enemy_pieces_classed:
            threatened_positions += enemy.generate_moves(position, board)

        for threatened_position in threatened_positions:
            board.occupancy_grid[threatened_position[0]][threatened_position[1]] = True


        self.visited_states = set() # stores king positions

        start_state = State(
            start_position,
            board,
            None
        )

        self.frontier.push(start_state)
        self.starting_state = start_state

    def get_child_states(self, state: State) -> Iterable[State]:
        child_states = []
        king = King()
        valid_moves = king.generate_moves(state.king_position, state.board)
        for position in valid_moves:
            child_states.append(
                State(
                    position,
                    state.board,
                    state
                )
            )

        return child_states

    def backtrack(self, state: State) -> Iterable[Move]:
        moves = []
        while state.parent_state is not None:
            moves.append([state.parent_state.king_position, state.king_position])
            state = state.parent_state
        return moves[::-1]

    def get_path(self) -> Iterable[Move]:
        # Place obstacles on occupancy_grid
        while not (self.frontier.is_empty()):
            # by default, we implement an early goal test
            state = self.frontier.pop()
            child_states = self.get_child_states(state)
            for child_state in child_states:
                if child_state.king_position in self.visited_states:
                    continue
                else:
                    for goal in self.goals:
                        if goal == child_state.king_position:
                            return self.backtrack(child_state)
                    self.frontier.push(child_state)
                    self.visited_states.add(child_state.king_position)
        
        return False    

    # # this function is mainly for debugging and making life easy
    # def print_path(self, path: Iterable[Move]) -> Iterable[Iterable[str]]:
    #     board = [[("X" if self.starting_state.board.occupancy_grid[j][i] else " ") for i in range(self.col_max)] for j in range(self.row_max)]

    #     for enemy, position in self.enemy_pieces:
    #         if enemy == "king":
    #             mark = "K"
    #         elif enemy == "Knight":
    #             mark = "H"
    #         else:
    #             mark = enemy[0]
    #         board[position[0]][position[1]] = mark

    #     for row in range(self.row_max):
    #         for col in range(self.col_max):
    #             if self.grid[row][col] == -1:
    #                 board[row][col] = "O"

    #     board[self.start_position[0]][self.start_position[1]] = "S"
        
    #     for goal in self.goals:
    #         board[goal[0]][goal[1]] = "G"

    #     for move in path[1:]:
    #         board[move[0][0]][move[0][1]] = "#"

    #     col_labels = "  "
    #     for i in range(0, self.col_max):
    #         col_labels += chr(ord('A') + i)
    #         col_labels += " "
    #     print(col_labels)
    #     print(" " + "-" * (self.col_max * 2 + 1))
    #     for row in range(self.row_max):
    #         string = f"{row}|"
    #         for col in range(self.col_max):
    #             string += board[row][col]
    #             string += " "
    #         string = string[:-1]
    #         string += "|"
    #         print(string)
    #     print(" " + "-" * (self.col_max * 2 + 1))


    #     return board       

#############################################################################
######## Implement Search Algorithm
#############################################################################
def search(rows, cols, grid, enemy_pieces, own_pieces, goals):
    if len(goals) == 0:
        return []

    searcher = Searcher(
        frontier = DFS_frontier(),
        start_position = own_pieces[0][1],
        row_max = rows,
        col_max = cols,
        enemy_pieces = enemy_pieces,
        goals = goals,
        grid = grid
    )
    path = searcher.get_path()
    if path == False:
        return []
    else:
        path
        # searcher.print_path(path)

        # convert path into the correct format
        path_correct_format = []
        for move in path:
            move_correct_format = []
            for position in move:
                move_correct_format.append((chr(position[1] + 97), position[0]))
            path_correct_format.append(move_correct_format)

        return path_correct_format

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
    grid = [[1 for j in range(cols)] for i in range(rows)] # Dictionary, label empty spaces as 1 (Default Step Cost)
    enemy_pieces = [] # List
    own_pieces = [] # List
    goals = [] # List

    handle.readline()  # Ignore number of obstacles
    for ch_coord in get_par(handle.readline()).split():  # Init obstacles
        r, c = from_chess_coord(ch_coord)
        grid[r][c] = -1 # Label Obstacle as -1

    handle.readline()  # Ignore Step Cost header
    line = handle.readline()
    while line.startswith("["):
        line = line[1:-2].split(",")
        r, c = from_chess_coord(line[0])
        grid[r][c] = int(line[1]) if grid[r][c] == 1 else grid[r][c] #Reinitialize step cost for coordinates with different costs
        line = handle.readline()
    
    line = handle.readline() # Read Enemy Position
    while line.startswith("["):
        line = line[1:-2]
        piece = add_piece(line)
        enemy_pieces.append(piece)
        line = handle.readline()

    # Read Own King Position
    line = handle.readline()[1:-2]
    piece = add_piece(line)
    own_pieces.append(piece)

    # Read Goal Positions
    for ch_coord in get_par(handle.readline()).split():
        r, c = from_chess_coord(ch_coord)
        goals.append((r, c))
    
    return rows, cols, grid, enemy_pieces, own_pieces, goals

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [piece, (r,c)]

def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)
    
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_DFS():
    testcase = sys.argv[1]
    rows, cols, grid, enemy_pieces, own_pieces, goals = parse(testcase)
    moves = search(rows, cols, grid, enemy_pieces, own_pieces, goals)
    return moves

if __name__ == "__main__":
    run_DFS()