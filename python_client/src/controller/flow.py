import pygame
from controller.input_handler import InputHandler

class GameController:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        self.input_handler = InputHandler()
        self.running = True

    def run_game(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.input_handler.handle_event(event, self.game)
            
            # Render game state
            self.renderer.render_board(self.game.board)
            clock.tick(30)