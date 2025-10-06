import pygame
from .paddle import Paddle
from .ball import Ball

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Game States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5  # Default
        
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 50)
        self.small_font = pygame.font.SysFont("Arial", 20)
        
        # Game state - Start with menu
        self.state = STATE_MENU
        self.winner = None

    def handle_input(self):
        """Handle keyboard input based on game state"""
        keys = pygame.key.get_pressed()
        
        if self.state == STATE_MENU:
            # Menu: Choose game mode
            if keys[pygame.K_3]:
                self.start_game(3)
            elif keys[pygame.K_5]:
                self.start_game(5)
            elif keys[pygame.K_7]:
                self.start_game(7)
        
        elif self.state == STATE_PLAYING:
            # Playing: Control paddle
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)
        
        elif self.state == STATE_GAME_OVER:
            # Game Over: Replay or exit
            if keys[pygame.K_r]:
                self.state = STATE_MENU
                self.reset_scores()
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

    def start_game(self, winning_score):
        """Start a new game with specified winning score"""
        self.winning_score = winning_score
        self.reset_scores()
        self.ball.reset()
        self.state = STATE_PLAYING

    def reset_scores(self):
        """Reset scores and winner"""
        self.player_score = 0
        self.ai_score = 0
        self.winner = None

    def update(self):
        """Update game logic - only when playing"""
        if self.state != STATE_PLAYING:
            return
        
        # Move ball
        self.ball.move()
        
        # Check paddle collision
        self.ball.check_collision(self.player, self.ai)

        # Check scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.check_game_over()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.check_game_over()
            self.ball.reset()

        # AI movement
        self.ai.auto_track(self.ball, self.height)

    def check_game_over(self):
        """Check if someone won"""
        if self.player_score >= self.winning_score:
            self.winner = "Player"
            self.state = STATE_GAME_OVER
        elif self.ai_score >= self.winning_score:
            self.winner = "AI"
            self.state = STATE_GAME_OVER

    def render(self, screen):
        """Render based on game state"""
        if self.state == STATE_MENU:
            self.render_menu(screen)
        elif self.state == STATE_PLAYING:
            self.render_game(screen)
        elif self.state == STATE_GAME_OVER:
            self.render_game_over(screen)

    def render_menu(self, screen):
        """Render main menu"""
        title = self.large_font.render("PING PONG", True, WHITE)
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 100))
        
        subtitle = self.font.render("Select Game Mode", True, WHITE)
        screen.blit(subtitle, (self.width // 2 - subtitle.get_width() // 2, 200))
        
        option1 = self.small_font.render("Press 3 - Best of 3", True, WHITE)
        option2 = self.small_font.render("Press 5 - Best of 5", True, WHITE)
        option3 = self.small_font.render("Press 7 - Best of 7", True, WHITE)
        
        screen.blit(option1, (self.width // 2 - option1.get_width() // 2, 300))
        screen.blit(option2, (self.width // 2 - option2.get_width() // 2, 350))
        screen.blit(option3, (self.width // 2 - option3.get_width() // 2, 400))
        
        controls = self.small_font.render("Controls: W/S to move paddle", True, GRAY)
        screen.blit(controls, (self.width // 2 - controls.get_width() // 2, 500))

    def render_game(self, screen):
        """Render the game"""
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))
        
        # Show game info
        info = self.small_font.render(f"First to {self.winning_score}", True, GRAY)
        screen.blit(info, (self.width // 2 - info.get_width() // 2, 10))

    def render_game_over(self, screen):
        """Render game over screen"""
        # Draw game in background
        self.render_game(screen)
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Winner text
        winner_text = self.large_font.render(f"{self.winner} Wins!", True, WHITE)
        screen.blit(winner_text, (self.width // 2 - winner_text.get_width() // 2, 200))
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.player_score} - {self.ai_score}", True, WHITE)
        screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 280))
        
        # Options
        replay = self.small_font.render("Press R - Play Again", True, WHITE)
        exit_text = self.small_font.render("Press ESC - Exit", True, WHITE)
        
        screen.blit(replay, (self.width // 2 - replay.get_width() // 2, 380))
        screen.blit(exit_text, (self.width // 2 - exit_text.get_width() // 2, 420))