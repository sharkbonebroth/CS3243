from ast import Call
from re import A, S
import sys
from typing import Iterable, Tuple, Callable
from __future__ import annotations
from collections import deque
from queue import PriorityQueue

Position = Tuple[int, int] # row, col
Move = Iterable[Position, Position] # position tuple, next position tuple

class Board:
    def __init__(
        self, 
        row_max: int, # holds the maximum number of rows
        col_max: int, # holds the maximum number of columns
        occupancy_grid: Iterable[Iterable[bool]], # Array of arrays containing where pieces are at. We are going to hack this grid to double as the movability_grid for the king
        cost_map: Iterable[Iterable[int]] # Array of arrays containing the cost of moving to a particular grid
        ):

        self.row_max = row_max
        self.col_max = col_max
        self.occupancy_grid = occupancy_grid
        self.cost_map = cost_map
        pass


#############################################################################
######## Piece
#############################################################################

def is_within_grid(position: Position, board: Board) -> bool:
    return not (position[0] < 0 or position[0] >= board.row_max or position[1] < 0 or position[1] >= board.col_max)

def is_occupied(position: Position, board: Board) -> bool:
    return (board.occupancy_grid[position[0]][position[1]])

def can_move_to(position: Position, board: Board) -> bool:
    print(position)
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
        cost_to_reach: float,
        cost_with_heuristic: float,
        board: Board, 
        parent_state: State = None,
        ):

        self.king_position = king_position
        self.cost_to_reach = cost_to_reach
        self.cost_with_heuristic = cost_with_heuristic
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
    def pop(self) -> State:
        return self.frontier.pop()

class Heap_frontier(Frontier):
    def __init__(self):
        self.frontier = PriorityQueue()

    def push(self, state: State) -> None:
        self.frontier.put(state.cost_with_heuristic, state)

    def pop(self) -> State:
        return self.frontier.get()

    def is_empty(self) -> bool:
        return self.frontier.empty()

#############################################################################
######## The SEARCHER
#############################################################################

class Searcher:
    def __init__(
            self, frontier: Frontier, 
            heuristic_function: Callable,
            start_position: Position,
            row_max: int,
            col_max: int,
            enemy_pieces: Iterable[Piece, Position],
            goals: Iterable[Position,],
            grid: Iterable[Iterable[int]]
        ):

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
            cost = grid
        )
        threatened_positions = []
        for enemy, position in enemy_pieces:
            threatened_positions += enemy.generate_moves(position, board)

        for threatened_position in threatened_positions:
            board.occupancy_grid[threatened_position[0]][threatened_position[1]] = True

        self.frontier = frontier
        self.heuristic_function = heuristic_function
        self.goals = goals

        self.visited_states = set() # stores king positions

        start_state = State(
            start_position,
            0,
            0,
            board,
            None
        )

        self.frontier.push(start_state)

    def get_child_states(self, state: State) -> Iterable[State]:
        child_states = []
        king = King()
        valid_moves = king.generate_moves(state.king_position, state.board)
        for position in valid_moves:
            cost_to_reach = state.cost_to_reach + state.board.cost_map[position[0]][position[1]]
            cost_with_heuristic = cost_to_reach + self.heuristic_function(position, state.board)
            child_states.append(
                State(
                    position,
                    cost_to_reach,
                    cost_with_heuristic,
                    state.board,
                    self
                )
            )

    def backtrack(self, state: State) -> Iterable[Move]:
        pass

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

class Searcher_late_GT(Searcher):
    def get_path(self) -> Iterable[Move]:
        while not (self.frontier.is_empty()):
            state = self.frontier.pop()
            # late goal test
            for goal in self.goals:
                if goal == state.king_position:
                    return self.backtrack(state)
            self.visited_states.add(state.king_position)
            child_states = self.get_child_states(state)
            for child_state in child_states:
                if child_state.king_position in self.visited_states:
                    continue
                else:
                    self.frontier.push(child_state)

#############################################################################
######## Misc helper functions
#############################################################################

def print_threatened_positions(board: Board, threatened: Iterable[Position]) -> None:
    out = [[" " for i in range(board.col_max)] for j in range(board.row_max)]
    for position in threatened:
        out[position[0]][position[1]] = "x"
    for row in out:
        string = ""
        for col in row:
            string += col
            string += " "
        print(string)


if __name__ == '__main__':
    # Run test codes for classes
    col_max = 10
    row_max = 8
    occupancy_grid = [[False for i in range(col_max)] for j in range(row_max)]
    movability_grid = [[False for i in range(col_max)] for j in range(row_max)]
    cost_map = [[1 for i in range(row_max)] for j in range(col_max)]
    board = Board(row_max, col_max, occupancy_grid, movability_grid, cost_map)
    occupancy_grid[1][3] = True
    occupancy_grid[1][2] = True
    occupancy_grid[3][5] = True
    piece = Princess()
    print_threatened_positions(board, piece.generate_moves(position=(5, 3), board=board))