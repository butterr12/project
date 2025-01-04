from model.board import Board
from model.piece import Mime
from view.renderer import Renderer
from controller.input_handler import InputHandler

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = "Player 1"
        self.counter = 0
        self.max_moves = 3
        self.winner = None
        self.game_over = False
        self.renderer = Renderer()
        self.input_handler = InputHandler()

    def switch_player(self):
        self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"
    
    def increment_counter(self):
        self.counter += 1
        if self.counter >= self.max_moves:
            self.switch_player()
            self.counter = 0
        print(self.counter)

    def get_counter(self) -> int:
        return self.counter

    def check_winner(self):
        print("entered check_winner")
        opponent = "Player 1" if self.current_player == "Player 2" else "Player 2"
        captured_pieces = self.board.get_captured_pieces(self.current_player)
        print(self.current_player)
        print(captured_pieces)

        for piece in captured_pieces:
            if isinstance(piece, Mime):
                self.winner = self.current_player
                self.game_over = True
                print(f"{self.winner} wins by capturing the opponent's Mime!")

                return self.winner
                

        #self.winner = self.board.check_for_winner()

    def reset(self):
        self.board = Board() 
        self.current_player = "Player 1"  
        self.counter = 0 
        self.max_moves = 3  
        self.winner = None  
        self.game_over = False
