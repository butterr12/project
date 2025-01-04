from model.piece import Piece, Mime, Goldqueen, Sighducky, Clefairy
from model.piece_initializer import PieceInitializer

class Board:
    def __init__(self):
        # 3x4 board with initial positions
        self.grid = [[None for _ in range(7)] for _ in range(8)]
        self.piece_initializer = PieceInitializer()
        self.initialize_pieces()
        self.captured_pieces_player1 = []
        self.captured_pieces_player2 = []

    def initialize_pieces(self):
        pieces = self.piece_initializer.initialize_pieces()  # Get pieces and their initial positions
        for x, y, piece in pieces:
            self.grid[x][y] = piece

    def move_piece(self, start, end):
        print("entered real move_piece")
        print(f"start[0]: {start[0]}, start[1]: {start[1]}")
        print(f"end[0]: {end[0]}, end[1]: {end[1]}")
        piece = self.grid[start[0]][start[1]]
        if piece is not None:
            target_piece = self.grid[end[0]][end[1]]
            if target_piece is not None and target_piece.owner != piece.owner:
                # Capture the opponent's piece
                if piece.owner == "Player 1":
                    self.captured_pieces_player1.append(target_piece)
                else:
                    self.captured_pieces_player2.append(target_piece)
                
                # Remove the captured piece from the board
                self.grid[end[0]][end[1]] = None
            self.grid[end[0]][end[1]] = piece
            self.grid[start[0]][start[1]] = None
    
    def get_captured_pieces(self, player):
        if player == "Player 1":
            return self.captured_pieces_player1
        else:
            return self.captured_pieces_player2
        #return []
    
    def print_captured_pieces(self):
        print("Captured pieces for Player 1:")
        for piece in self.captured_pieces_player1:
            print(piece)
        print("Captured pieces for Player 2:")
        for piece in self.captured_pieces_player2:
            print(piece)

    # def check_for_winner(self):
        # Check for win conditions
        # return None  # Placeholder
