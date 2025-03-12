import pygame
import consts
from cursor import Cursor

class Paddle:
    def __init__(self, x_corner : int, y_corner : int, is_human : bool = True, color : str = '#FFFFFF') -> None:
        self.color = color
        self.is_human = is_human
        self.hitbox = pygame.Rect(x_corner, y_corner, consts.PADDLE_WIDTH, consts.PADDLE_LENGTH)
        self.starting_position_rectangle = pygame.Rect(self.hitbox)
        self.points = 0

    def draw(self, surface : pygame.SurfaceType) -> None:
        pygame.draw.rect(surface, 
                         self.color,
                         self.hitbox)

    def move(self, input : tuple[bool]):
        if self.is_human:
            if input[consts.HUMAN_PLAYER_CONTROLS["right"]]: 
                self.move_right()
            if input[consts.HUMAN_PLAYER_CONTROLS["left"]]:
                self.move_left()

    def move_to_cursor(self, cursor : Cursor):
        cursor_hitbox = cursor.get_hitbox()
        if self.hitbox.centerx < cursor_hitbox.x:
            self.move_right()
        if self.hitbox.centerx > cursor_hitbox.x:
            self.move_left()

    def move_left(self):
        if self.hitbox.left - consts.PADDLE_SPEED > 0:
            self.hitbox.left = self.hitbox.left - consts.PADDLE_SPEED

    def move_right(self):
        if self.hitbox.right + consts.PADDLE_SPEED < consts.WINDOW_WIDTH:
            self.hitbox.right = self.hitbox.right + consts.PADDLE_SPEED

    def get_hitbox(self) -> pygame.Rect:
        return self.hitbox
    
    def reset(self):
        self.hitbox = pygame.Rect(self.starting_position_rectangle)
        self.points = 0
