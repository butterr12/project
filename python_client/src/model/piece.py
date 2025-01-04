from abc import ABC, abstractmethod
from typing import List, Tuple

class Piece(ABC):
    def __init__(self, name: str, owner: str):
        self.name = name
        self.owner = owner

    def __str__(self):
        return f"{self.name} ({self.owner})"

    @abstractmethod
    def valid_moves(self, position: Tuple[int, int], board) -> List[Tuple[int, int]]:
        """Return a list of valid moves based on the piece type."""
        pass

    def _calculate_moves(self, position: Tuple[int, int], directions: List[Tuple[int, int]], board) -> List[Tuple[int, int]]:
        moves = []
        for dx, dy in directions:
            new_x = position[0] + dx
            new_y = position[1] + dy
            print(f"pos[0]: {position[0]}, pos[1]: {position[1]}")
            print(f"new_x: {new_x}, new_y: {new_y}")
            print(f"board_grid[0]: {len(board.grid[0])}")
            print(f"board_grid: {len(board.grid)}")
            if 0 <= new_x < len(board.grid) and 0 <= new_y < len(board.grid[0]):
                if board.grid[new_x][new_y] is None or board.grid[new_x][new_y].owner != self.owner:
                    moves.append((new_x, new_y))
        return moves

class Mime(Piece):
    def __init__(self, owner: str):
        super().__init__("Mime", owner)

    def valid_moves(self, position: Tuple[int, int], board) -> List[Tuple[int, int]]:
        # valid moves are:
        # (0,0) (0,1) (0,2)        (-1,-1) (-1,0) (-1,1)
        # (1,0) (1,1) (1,2)   ->   (0,-1)    x    (0,1)
        # (2,0) (2,1) (2,2)        (1,-1)  (1,0)  (1,1)
        # assuming Mime (x) can move in all directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return self._calculate_moves(position, directions, board)

class Goldqueen(Piece):
    def __init__(self, owner: str):
        super().__init__("Goldqueen", owner)

    def valid_moves(self, position: Tuple[int, int], board) -> List[Tuple[int, int]]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._calculate_moves(position, directions, board)

class Sighducky(Piece):
    def __init__(self, owner: str):
        super().__init__("Sighducky", owner)

    def valid_moves(self, position: Tuple[int, int], board) -> List[Tuple[int, int]]:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._calculate_moves(position, directions, board)

class Monkey(Piece):
    def __init__(self, owner: str):
        super().__init__("Monkey", owner)

    def valid_moves(self, position: Tuple[int, int], board) -> List[Tuple[int, int]]:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._calculate_moves(position, directions, board)

class Charman(Piece):
    def __init__(self, owner: str):
        super().__init__("Charman", owner)

    def valid_moves(self, position: Tuple[int, int], board) -> List[Tuple[int, int]]:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._calculate_moves(position, directions, board)

class Clefairy(Piece):
    def __init__(self, owner: str):
        super().__init__("Clefairy", owner)

    def valid_moves(self, position: Tuple[int, int], board) -> List[Tuple[int, int]]:
        if self.owner == "Player 1":
            directions = [(1, 0)] 
        else:
            directions = [(-1, 0)] 
        return self._calculate_moves(position, directions, board)
