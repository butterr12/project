import pygame
import os
from typing import List, Tuple
from model.piece import Piece  

class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((950, 700), pygame.RESIZABLE)
        pygame.display.set_caption("Dobutsu Shogi")
        self.images = self.load_piece_images()
        self.rows = 8  # Number of rows on the board
        self.cols = 7
        #self.cell_size = 100

    # def load_piece_images(self):
    #     """Load images for each piece from the assets folder."""
    #     assets_path = os.path.join(os.path.dirname(__file__), "assets")
        
    #     images = {
    #         "Charman": pygame.image.load(os.path.join(assets_path, "charman.png")),
    #         "Clefairy": pygame.image.load(os.path.join(assets_path, "clefairy.png")),
    #         "Goldqueen": pygame.image.load(os.path.join(assets_path, "goldqueen.png")),
    #         "Mime": pygame.image.load(os.path.join(assets_path, "mime.png")),
    #         "Monkey": pygame.image.load(os.path.join(assets_path, "monkey.png")),
    #         "Sighducky": pygame.image.load(os.path.join(assets_path, "sighducky.png")),
    #     }
    #     for key in images:
    #         images[key] = pygame.transform.scale(images[key], (80, 80))
    #     return images

    def load_piece_images(self):
        """Load images for each piece for both players."""
        assets_path = os.path.join(os.path.dirname(__file__), "assets")
        
        images = {
            "Player 1": {
                "Charman": pygame.image.load(os.path.join(assets_path, "player1_charman.png")),
                "Clefairy": pygame.image.load(os.path.join(assets_path, "player1_clefairy.png")),
                "Goldqueen": pygame.image.load(os.path.join(assets_path, "player1_goldqueen.png")),
                "Mime": pygame.image.load(os.path.join(assets_path, "player1_mime.png")),
                "Monkey": pygame.image.load(os.path.join(assets_path, "player1_monkey.png")),
                "Sighducky": pygame.image.load(os.path.join(assets_path, "player1_sighducky.png")),
            },
            "Player 2": {
                "Charman": pygame.image.load(os.path.join(assets_path, "player2_charman.png")),
                "Clefairy": pygame.image.load(os.path.join(assets_path, "player2_clefairy.png")),
                "Goldqueen": pygame.image.load(os.path.join(assets_path, "player2_goldqueen.png")),
                "Mime": pygame.image.load(os.path.join(assets_path, "player2_mime.png")),
                "Monkey": pygame.image.load(os.path.join(assets_path, "player2_monkey.png")),
                "Sighducky": pygame.image.load(os.path.join(assets_path, "player2_sighducky.png")),
            }
        }
        
        for player, pieces in images.items():
            for key in pieces:
                pieces[key] = pygame.transform.scale(pieces[key], (80, 80))
        return images


    def calculate_cell_size(self):
        """Calculate the cell size dynamically based on the window size."""
        screen_width, screen_height = pygame.display.get_window_size()
        right_margin = 300
        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width()

        # Calculate available space for the board
        available_width = screen_width - right_margin
        available_height = screen_height

        # Calculate cell size to fit within available space
        cell_width = available_width // self.cols
        cell_height = available_height // self.rows
        self.cell_size = min(cell_width, cell_height)

        return self.cell_size
        # print(screen_width)
        # print(screen_height)
        # print(cell_width)
        # print(cell_height)
        # print(self.cell_size)
    
    def get_cell_size(self):
        """Ensure cell size is calculated and return it."""
        self.calculate_cell_size()  # Recalculate before returning, in case the window size changed.
        return self.cell_size

    def render_board(self, board, game, valid_moves: List[Tuple[int, int]] = None, selected_piece: Piece = None):
        """Renders the board with optional highlights for valid moves, centered on the screen."""
        self.calculate_cell_size()
        self.screen.fill((255, 255, 255))  # Background color

        right_margin = 300
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()

        # Calculate available space for the board
        available_width = screen_width - right_margin
        available_height = screen_height

        # Calculate cell size to fit within available space
        cell_width = available_width // self.cols
        cell_height = available_height // self.rows
        self.cell_size = min(cell_width, cell_height)

        # Calculate offsets for centering the board
        board_width = self.cell_size * self.cols
        board_height = self.cell_size * self.rows
        x_offset = (available_width - board_width) // 2
        y_offset = (screen_height - board_height) // 2
        

        for y, row in enumerate(board.grid):
            for x, piece in enumerate(row):
                starting_x = x * self.cell_size + x_offset
                starting_y = y * self.cell_size + y_offset
                rect = pygame.Rect(
                    starting_x,
                    starting_y,
                    self.cell_size,
                    self.cell_size
                )

                # Highlight valid moves
                if piece and piece.protected: #lalagyan ko pa ng or opponent.piece.protected
                    pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)  # Default border for the cell
                elif valid_moves and (y, x) in valid_moves:
                    pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
                    inner_rect = rect.inflate(-4, -4)
                    pygame.draw.rect(self.screen, (0, 255, 0), inner_rect)
                elif board.get_valid_dropping_points and selected_piece in board.get_captured_pieces(game.current_player):
                    valid_list = board.get_valid_dropping_points(board.get_all_empty_cells(), board.get_invalid_dropping_points())
                    if (y, x) in valid_list:
                        pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
                        inner_rect = rect.inflate(-4, -4)
                        pygame.draw.rect(self.screen, (0, 0, 200), inner_rect)
                    else:
                        pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
                else:
                    pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
                # Draw the piece if present
                # if piece:
                #     image = self.images.get(piece.name)
                #     if image:
                #         image_size = self.cell_size - 20
                #         image = pygame.transform.scale(image, (image_size, image_size))
                #         self.screen.blit(
                #             image,
                #             (x * self.cell_size + x_offset + (self.cell_size - image_size) // 2,
                #             y * self.cell_size + y_offset + (self.cell_size - image_size) // 2)
                #         )

                if piece:
                    player_key = piece.owner  # Example: "Player 1" or "Player 2"
                    image = self.images[player_key].get(piece.name)
                    if image:
                        image_size = self.cell_size - 20
                        image = pygame.transform.scale(image, (image_size, image_size))
                        self.screen.blit(
                            image,
                            (x * self.cell_size + x_offset + (self.cell_size - image_size) // 2,
                            y * self.cell_size + y_offset + (self.cell_size - image_size) // 2)
                        )

        
        self.render_captured_pieces(board)
        #self.render_highlight
        pygame.display.flip()

    def render_winner(self, winner: str):
        """
        Renders a "Player _ wins" message with a semi-transparent white background.

        Args:
            winner (str): The name of the winning player (e.g., "Player 1" or "Player 2").
        """
        print(f"Rendering winner: {winner}")  
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 153))
        font = pygame.font.Font(None, 50)
        text = font.render(f"{winner} wins!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        #pygame.display.update()
    def render_draw(self):
        """
        Renders a "Player _ wins" message with a semi-transparent white background.

        Args:
            winner (str): The name of the winning player (e.g., "Player 1" or "Player 2").
        """
        print(f"Rendering draw")  
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 153))
        font = pygame.font.Font(None, 50)
        text = font.render(f"Game is draw!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def render_captured_pieces(self, board):
        """Render captured pieces beside the main board."""
        self.captured_piece_rects = {"Player 1": [], "Player 2": []}
        self.calculate_cell_size()
        cell_size = self.cell_size
        right_margin = 300
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()

        # Calculate available space for the board
        available_width = screen_width - right_margin
        available_height = screen_height

        # Calculate cell size to fit within available space
        cell_width = available_width // self.cols
        cell_height = available_height // self.rows
        self.cell_size = min(cell_width, cell_height)

        # Calculate offsets for centering the board
        board_width = self.cell_size * self.cols
        board_height = self.cell_size * self.rows
        self.x_offset = (available_width - board_width) // 2
        self.y_offset = (screen_height - board_height) // 2

        # Define captured pieces area
        captured_area_start_x = board_width + self.x_offset + 20  # Right of the board
        captured_area_start_y = self.y_offset

        # Calculate maximum pieces per row dynamically
        max_pieces_per_row = max(3, min(5, (screen_width - captured_area_start_x) // cell_size))

        # Render text for Player 1's captured pieces
        font = pygame.font.Font(None, cell_size // 3)
        player1_text = font.render("Captured Pieces (Player 1)", True, (0, 0, 0))  # Black text
        player1_text_x = captured_area_start_x
        player1_text_y = captured_area_start_y + 10  # A bit of padding above the pieces
        self.screen.blit(player1_text, (player1_text_x, player1_text_y))

        # Render Player 1's captured pieces (top-right section)
        y_offset = player1_text_y + 30  # Add padding below the text
        for i, piece in enumerate(board.captured_pieces_player1):
            row = i // max_pieces_per_row
            col = i % max_pieces_per_row
            piece_x = captured_area_start_x + col * cell_size
            piece_y = y_offset + row * cell_size

            image = self.images.get(piece.owner, {}).get(piece.__class__.__name__)
            if image:
                image = pygame.transform.scale(image, (cell_size - 20, cell_size - 20))
                rect = self.screen.blit(image, (piece_x, piece_y))
                self.captured_piece_rects["Player 1"].append((piece, rect))

        # Render text for Player 2's captured pieces
        player2_text = font.render("Captured Pieces (Player 2)", True, (0, 0, 0))  # Black text
        player2_text_x = captured_area_start_x
        # print(f"cell_size for rendering: {cell_size}")
        player2_text_y = (cell_size * (self.rows//2)) + y_offset - 25
        self.screen.blit(player2_text, (player2_text_x, player2_text_y))

        # Render Player 2's captured pieces (below Player 1's section)
        y_offset = player2_text_y + 30  # Add padding below the text
        for i, piece in enumerate(board.captured_pieces_player2):
            row = i // max_pieces_per_row
            col = i % max_pieces_per_row
            piece_x = captured_area_start_x + col * cell_size
            piece_y = y_offset + row * cell_size

            image = self.images.get(piece.owner, {}).get(piece.__class__.__name__)
            if image:
                image = pygame.transform.scale(image, (cell_size - 20, cell_size - 20))
                rect = self.screen.blit(image, (piece_x, piece_y))
                self.captured_piece_rects["Player 2"].append((piece, rect))

        # print(f"captured_rects: {self.captured_piece_rects}")
        return self.captured_piece_rects

    def render_play_again_button(self):
        button_width, button_height = 200, 50
        button_x = (self.screen.get_width() - button_width) // 2
        button_y = (self.screen.get_height() // 2) + 30  

        self.play_again_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, (0, 128, 0), self.play_again_button_rect) 

        font = pygame.font.Font(None, 30)
        text_surface = font.render("Play Again", True, (255, 255, 255))  
        text_rect = text_surface.get_rect(center=self.play_again_button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def highlight_flag(self, selected_piece, captured_pieces):
        if selected_piece and selected_piece in captured_pieces:
            return True
        else:
            return False
