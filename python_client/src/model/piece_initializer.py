from model.piece import Piece, Mime, Goldqueen, Sighducky, Clefairy, Monkey, Charman
from typing import List, Tuple

class PieceInitializer:
    @staticmethod
    def initialize_pieces() -> List[Tuple[int, int, Piece]]:
        pieces = [
            (0, 0, Goldqueen("Player 1")),
            (7, 0, Goldqueen("Player 2")),
            (0, 1, Sighducky("Player 1")),
            (7, 1, Sighducky("Player 2")),
            (0, 2, Mime("Player 1")),
            (7, 2, Mime("Player 2")),
            (0, 3, Monkey("Player 1")),
            (7, 3, Monkey("Player 2")),
            (0, 4, Charman("Player 1")),
            (7, 4, Charman("Player 2")),
            (0, 5, Sighducky("Player 1")),
            (7, 5, Sighducky("Player 2")),
            (0, 6, Goldqueen("Player 1")),
            (7, 6, Goldqueen("Player 2")),
            (1, 1, Clefairy("Player 1")),
            (1, 3, Sighducky("Player 1")),
            (1, 5, Clefairy("Player 1")),
            (6, 1, Clefairy("Player 2")),
            (6, 3, Sighducky("Player 2")),
            (6, 5, Clefairy("Player 2")),
        ]
        return pieces
