import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.max_speed = 8  # Limit maximum speed to prevent tunneling
        self.collision_cooldown = 0  # Prevent multiple collisions per hit

    def move(self):
        # Decrease collision cooldown
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1
        
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision (top and bottom)
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            return 'wall'
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            return 'wall'
        
        return None

    def check_collision(self, player, ai):
        """Enhanced collision detection with position correction and cooldown"""
        
        # Only check collision if cooldown expired
        if self.collision_cooldown > 0:
            return None
        
        ball_rect = self.rect()
        
        # Check player paddle collision
        if ball_rect.colliderect(player.rect()):
            # Position correction: move ball outside paddle
            if self.velocity_x < 0:  # Ball moving left
                self.x = player.x + player.width
            
            # Reverse and slightly increase velocity
            self.velocity_x = abs(self.velocity_x) * 1.05
            
            # Add spin based on where ball hits paddle
            paddle_center = player.y + player.height / 2
            ball_center = self.y + self.height / 2
            offset = (ball_center - paddle_center) / (player.height / 2)
            self.velocity_y += offset * 2
            
            # Clamp velocities
            self.velocity_x = min(self.velocity_x, self.max_speed)
            self.velocity_y = max(-self.max_speed, min(self.velocity_y, self.max_speed))
            
            # Set cooldown to prevent multiple hits
            self.collision_cooldown = 5
            return 'paddle'
        
        # Check AI paddle collision
        elif ball_rect.colliderect(ai.rect()):
            # Position correction: move ball outside paddle
            if self.velocity_x > 0:  # Ball moving right
                self.x = ai.x - self.width
            
            # Reverse and slightly increase velocity
            self.velocity_x = -abs(self.velocity_x) * 1.05
            
            # Add spin based on where ball hits paddle
            paddle_center = ai.y + ai.height / 2
            ball_center = self.y + self.height / 2
            offset = (ball_center - paddle_center) / (ai.height / 2)
            self.velocity_y += offset * 2
            
            # Clamp velocities
            self.velocity_x = max(self.velocity_x, -self.max_speed)
            self.velocity_y = max(-self.max_speed, min(self.velocity_y, self.max_speed))
            
            # Set cooldown to prevent multiple hits
            self.collision_cooldown = 5
            return 'paddle'
        
        return None

    def reset(self):
        """Reset ball to center with random direction"""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.collision_cooldown = 0

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)