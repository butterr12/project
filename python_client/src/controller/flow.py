import pygame
from controller.input_handler import InputHandler

class GameController:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        self.input_handler = InputHandler()
        self.running = True
        self.winner_message_rendered = False
        self.play_again_button_rendered = False
        self.wait_after_game_over = True

    def run_game(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.game.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.renderer.play_again_button_rect.collidepoint(mouse_pos):
                        self.reset_game()  
                else:
                    self.input_handler.handle_event(event, self.game)
            
            if not self.game.game_over:
                self.renderer.render_board(
                    self.game.board, 
                    self.game,
                    valid_moves=self.input_handler.valid_moves,  
                    selected_piece=self.input_handler.selected_piece  
                )
            else:
                # if not self.play_again_button_rendered:
                #     self.renderer.render_winner(self.game.winner)
                #     self.renderer.render_play_again_button()
                #     self.play_again_button_rendered = True

                if self.wait_after_game_over:
                    self.renderer.render_board(
                        self.game.board,
                        self.game,
                        valid_moves=self.input_handler.valid_moves,  
                        selected_piece=self.input_handler.selected_piece  
                    ) # force to show final board state
                    pygame.display.flip()  
                    self.wait_after_game_over = False
                elif not self.play_again_button_rendered:
                    if self.game.check_draw():  # Check if the game is a draw
                        self.renderer.render_draw()  # Render draw visually
                    elif self.game.winner:  # If there's a winner
                        self.renderer.render_winner(self.game.winner)
                    self.renderer.render_play_again_button() 
                    self.play_again_button_rendered = True
             
            pygame.display.flip()
            clock.tick(30)

    def reset_game(self):
        """Reset the game state and input handler."""
        self.game.reset()  # Reset the game state
        self.input_handler.reset()  # Reset the input handler
        self.winner_message_rendered = False
        self.play_again_button_rendered = False
        self.wait_after_game_over = True