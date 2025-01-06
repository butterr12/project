import pygame
from model.board import Board
from model.piece import Piece
# from model.game import Game
# from project.python_client.src.model import board
from view.renderer import Renderer

class InputHandler:
    def __init__(self):
        self.selected_piece = None
        self.valid_moves = [] 
        self.winner_rendered = False 
        self.draw_rendered = False
        self.renderer = Renderer()
        self.checkmate_count = 0

    def handle_event(self, event, game):
        if game.game_over:
            if game.check_draw():  # Check if the game is a draw
                if not self.draw_rendered:
                    print("Game over! It's a draw!")
                    # self.renderer.render_draw()  # Render a draw visually if implemented
                    self.draw_rendered = True
            elif game.winner:  # Check if there's a winner
                if not self.winner_rendered:
                    print(f"Game over! {game.winner} wins!")
                    # self.renderer.render_winner(game.winner)  # Render the winner visually
                    self.winner_rendered = True

            
        if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
            #cell_size = self.renderer.get_cell_size()
            # print(cell_size)

            

            right_margin = 300
            screen_height = self.renderer.screen.get_height()
            screen_width = self.renderer.screen.get_width()

            # Calculate available space for the board
            available_width = screen_width - right_margin
            available_height = screen_height

            # Calculate cell size to fit within available space
            cell_width = available_width // self.renderer.cols
            cell_height = available_height // self.renderer.rows
            self.cell_size = min(cell_width, cell_height)

            # Calculate offsets for centering the board
            board_width = self.cell_size * self.renderer.cols
            board_height = self.cell_size * self.renderer.rows
            x_offset = (available_width - board_width) // 2
            y_offset = (screen_height - board_height) // 2
            # board_width = self.renderer.screen.get_width() - x_offset*2
            # board_height = self.renderer.screen.get_height() - x_offset*2

            x, y = event.pos
            print(f"x: {x}")
            print(f"y: {y}")
            print(f"board width: {board_width}")
            print(f"board height: {board_height}")
            print(f"x_offset: {x_offset}")
            print(f"y_offset: {y_offset}")
            screen_height = self.renderer.screen.get_height()
            screen_width = self.renderer.screen.get_width()
            print(f"screen_height: {screen_height}")
            print(f"screen_width: {screen_width}")
            grid_x, grid_y = (y - y_offset) // self.cell_size, (x - x_offset) // self.cell_size
            print(f"row: {grid_x}")
            print(f"col: {grid_y}")

            grid_x, grid_y = (y - y_offset) // self.cell_size, (x - x_offset) // self.cell_size
            captured_piece_rects = game.renderer.render_captured_pieces(game.board)
            print(f"captured_piece_rects: {captured_piece_rects}")

            # Check if the click is outside the board
            if not (0 <= grid_x < len(game.board.grid) and 0 <= grid_y < len(game.board.grid[0])):
                # Check if the click is on Player 1's captured pieces
                mouse_pos = event.pos
                for piece, rect in captured_piece_rects["Player 1"]:
                    if rect.collidepoint(mouse_pos):
                        # Check if the same piece is selected twice
                        if self.selected_piece == piece:
                            print(f"Deselected piece: {self.selected_piece.name}")
                            self.selected_piece = None  # Deselect the piece
                            self.valid_moves = []  # Clear valid moves
                            #game.renderer.clear_highlights()
                            return
                        else:
                            if self.selected_piece:  # Reset the previously selected piece
                                print(f"Deselected piece: {self.selected_piece.name}")
                            print(f"Player 1 selected {piece.name}")
                            self.selected_piece = piece
                            #game.renderer.selected_piece_from_controller()
                            game.renderer.highlight_flag(self.selected_piece, game.board.get_captured_pieces(game.current_player))
                            return

                # Check if the click is on Player 2's captured pieces
                for piece, rect in captured_piece_rects["Player 2"]:
                    if rect.collidepoint(mouse_pos):
                        # Check if the same piece is selected twice
                        if self.selected_piece == piece:
                            print(f"Deselected piece: {self.selected_piece.name}")
                            self.selected_piece = None  # Deselect the piece
                            self.valid_moves = []  # Clear valid moves
                            #game.renderer.clear_highlights()
                            return
                        else:
                            if self.selected_piece:  # Reset the previously selected piece
                                print(f"Deselected piece: {self.selected_piece.name}")
                            print(f"Player 2 selected {piece.name}")
                            self.selected_piece = piece
                            #game.renderer.highlight_flag()
                            return

                # If the click is not on the board or captured pieces, do nothing
                print("Choose within the grid or on captured pieces.")
                return

            #print(f"selected piece: {self.selected_piece}")
            #print(f"capytured pieces: {game.board.get_captured_pieces(game.current_player)}")
            game.board.print_captured_pieces()
            if self.selected_piece and self.selected_piece in game.board.get_captured_pieces(game.current_player):
                print("inside")
                if 0 <= grid_x < len(game.board.grid) and 0 <= grid_y < len(game.board.grid[0]):
                    #game.renderer.highlight_flag(self.selected_piece,  game.board.get_captured_pieces(game.current_player))
                    success = game.board.drop_captured_piece(game.current_player, self.selected_piece, (grid_x, grid_y), game)
                    if success:
                        print(f"{self.selected_piece.name} redeployed to ({grid_x}, {grid_y}).")
                        self.selected_piece = None
                        self.valid_moves = []  # Reset valid moves after redeployment
                        return
                    else:
                        print("Redeployment failed.")
                else:
                    print("Invalid position for redeployment.")
                return

            clicked_piece = game.board.grid[grid_x][grid_y]
            game.print_all_moves_opp()
            game.checkmate_opp()
            game.get_all_valid_moves_protected_pieces()



            if clicked_piece and clicked_piece.owner == game.current_player:
                # reselect new piece if misclicked/change of mind
                self.selected_piece = clicked_piece
                self.valid_moves = self.selected_piece.valid_moves((grid_x, grid_y), game.board)
                self.orig_coords = (grid_x, grid_y)
                print(f"Switched to new piece: {self.selected_piece}")
                print(f"Valid moves: {self.valid_moves}")
                    
            elif self.selected_piece:
                print(self.selected_piece)
                # Check if the clicked position is a valid move
                if (grid_x, grid_y) in self.valid_moves:
                    print(grid_x)
                    print(grid_y)
                    print("entered movepiece")
                    game.board.move_piece(self.orig_coords, (grid_x, grid_y), game)
                    # game.get_available_pieces_and_moves() # wala na to
                    if game.checkmate():
                        self.checkmate_count += 1 
                    print(f"check_count: {self.checkmate_count}")
                    # Check winner after opponent's turn
                    move_counter = game.get_counter()
                    if game.checkmate_opp() and move_counter >= 2:
                        game.check_winner()
                        print(f"Game over! {game.winner} wins!")
                    else:
                        # Switch to opponent's turn
                        print(f"proceed as usual.")
                    # game.check_winner()
                    # Check if the opponent is in checkmate after the move
                    # previous_player = game.current_player
                    move_status = game.board.move_status()
                    print(f"move_status: {move_status}")
                    if move_status:
                        game.increment_counter()
                        print(f"hatdog")
                    game.board.print_captured_pieces()
                    self.selected_piece = None
                    self.valid_moves = []  # Reset valid moves after the move
                    self.orig_coords = None
                else:
                    print("Invalid move!")
            else:
                # Select the piece if it belongs to the current player
                piece = game.board.grid[grid_x][grid_y]
                if piece and piece.owner == game.current_player:
                    self.selected_piece = piece
                    print(self.selected_piece)
                    # Calculate valid moves as soon as the piece is selected
                    self.valid_moves = self.selected_piece.valid_moves((grid_x, grid_y), game.board)
                    self.orig_coords = [grid_x, grid_y]
                    print(f"Valid moves: {self.valid_moves}")
                else:
                    print("No valid piece selected or wrong player!")

    def reset(self):

        self.selected_piece = None
        self.valid_moves = []
        self.winner_message_rendered = False
