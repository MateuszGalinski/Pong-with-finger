import pygame
import consts
import random

from paddle import Paddle


class Block:
    def __init__(self, passable=True, color="#FFD700"):
        self.width = consts.BLOCK_WIDTH
        self.height = consts.BLOCK_HEIGHT
        self.color = color
        self.passable = passable
        self.reset()
        self.active = False

    def reset(self):
        self.x = random.randint(consts.WINDOW_WIDTH // 4, 3 * consts.WINDOW_WIDTH // 4)
        self.y = random.randint(consts.WINDOW_HEIGH // 4, 3 * consts.WINDOW_HEIGH // 4)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.active = True

    def draw(self, surface: pygame.SurfaceType) -> None:
        if self.active:
            pygame.draw.rect(surface, self.color, self.hitbox)

    def check_collision(self, ball_hitbox: pygame.Rect, last_player_touched: Paddle) -> bool:
        if self.active and self.hitbox.colliderect(ball_hitbox):
            if not self.passable:
                pass
            last_player_touched.points += consts.BLOCK_POINTS
            self.active = False
            return True
        return False

    def is_active(self) -> bool:
        return self.active
