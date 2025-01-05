from model.piece import Piece, Mime, Goldqueen, Sighducky, Clefairy
from model.piece_initializer import PieceInitializer
from copy import deepcopy

class Board:
    def __init__(self):
        # 3x4 board with initial positions
        self.grid = [[None for _ in range(7)] for _ in range(8)]
        self.piece_initializer = PieceInitializer()
        self.initialize_pieces()
        self.captured_pieces_player1 = []
        self.captured_pieces_player2 = []
        self.captured_positions_player1 = []
        self.captured_positions_player2 = []
        self.moved_piece = False

    def initialize_pieces(self):
        pieces = self.piece_initializer.initialize_pieces()  # Get pieces and their initial positions
        for x, y, piece in pieces:
            self.grid[x][y] = piece

    def move_piece(self, start, end, game):
        print("entered real move_piece")
        print(f"start[0]: {start[0]}, start[1]: {start[1]}")
        print(f"end[0]: {end[0]}, end[1]: {end[1]}")
        piece = self.grid[start[0]][start[1]]
        if piece is not None:
            target_piece = self.grid[end[0]][end[1]]

            # Simulate the move
            temp_grid = deepcopy(self.grid)
            temp_grid[end[0]][end[1]] = piece
            temp_grid[start[0]][start[1]] = None

            # Check if the move puts the player's own protected pieces in danger
            protected_pieces = [
                (p, (r, c)) for r, row in enumerate(temp_grid) for c, p in enumerate(row)
                if p and p.protected and p.owner == piece.owner
            ]
            opponent_moves = game.get_available_pieces_and_moves_opp()

            # Check if any protected piece is threatened
            if piece.protected and end in [move for moves in opponent_moves.values() for move in moves]:
                print(f"Move denied: Moving to {end} puts a protected piece in danger.")
                self.moved_piece = False
                return

            # Prevent protected pieces from capturing opponents' pieces
            if target_piece is not None and piece.protected:
                print(f"Move denied: Protected piece at {start} cannot capture opponent's piece.")
                self.moved_piece = False
                return

            # Prevent opponents from capturing protected pieces
            if target_piece is not None and target_piece.protected and target_piece.owner != piece.owner:
                print(f"Move denied: Cannot capture protected piece at {end}.")
                self.moved_piece = False
                return

            if target_piece is not None and target_piece.owner != piece.owner:
                # Capture the opponent's piece
                if piece.owner == "Player 1":
                    self.captured_pieces_player1.append(target_piece)
                    self.captured_positions_player1.append(end)
                else:
                    self.captured_pieces_player2.append(target_piece)
                    self.captured_positions_player2.append(end)
                # Remove the captured piece from the board
                self.grid[end[0]][end[1]] = None
            self.grid[end[0]][end[1]] = piece
            self.grid[start[0]][start[1]] = None
            self.moved_piece = True
            
    
    def get_captured_pieces(self, player):
        if player == "Player 1":
            return self.captured_pieces_player1
        else:
            return self.captured_pieces_player2
        #return []
    
    def get_captured_pieces_position(self, player):
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
    
    def move_status(self):
        return self.moved_piece

    # def check_for_winner(self):
        # Check for win conditions
        # return None  # Placeholder
