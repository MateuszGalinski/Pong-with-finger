import pygame
import consts
from paddle import Paddle

class Ball:
    def __init__(self, color : str = "#FFFFFF"):
        x_center = consts.WINDOW_WIDTH/2
        y_center = consts.WINDOW_HEIGH/2
        self.hitbox = pygame.Rect(x_center - consts.BALL_RADIUS, 
                                  y_center - consts.BALL_RADIUS, 
                                  consts.BALL_RADIUS * 2, 
                                  consts.BALL_RADIUS * 2) # calculates rectangle for initial hitbox
        self.starting_position_rectangle = pygame.Rect(self.hitbox)

        self.color = color
        self.direction = consts.BALL_INITIAL_DIRECTION # format [x,y] where -1 <= x,y <= 1 

    def draw(self, surface : pygame.SurfaceType) -> None:
        pygame.draw.circle(surface, self.color, (self.hitbox.centerx, self.hitbox.centery), consts.BALL_RADIUS)

    def move(self) -> None:
        self.hitbox.centerx = self.hitbox.centerx + self.direction[0] * consts.BALL_SPEED
        self.hitbox.centery = self.hitbox.centery + self.direction[1] * consts.BALL_SPEED

    def check_colision(self, paddle : Paddle, bounce_off_top_edge : bool = False) -> None:
        if self.hitbox.right >= consts.WINDOW_WIDTH:
            self.direction[0] = -self.direction[0]
            self.hitbox.right = consts.WINDOW_WIDTH - 1

        if self.hitbox.left <= consts.WINDOW_LEFT_SIDE:
            self.direction[0] = -self.direction[0]
            self.hitbox.left = consts.WINDOW_SAFE_ZONE_LEFT

        paddle_hitbox = paddle.get_hitbox()

        # print("PADDLE TOP: " + str(paddle_hitbox.top))
        # print("BALL HITBOX CENTERY")

        if(self.hitbox.colliderect(paddle_hitbox)):
            if paddle_hitbox.centery > consts.WINDOW_HEIGH/2: # assumes player is always on the bottom
                self.player_collision(paddle_hitbox)
            else:
                self.computer_collision(paddle_hitbox)
            
        if bounce_off_top_edge:
            if self.hitbox.top < 0:
                self.direction[1] = -self.direction[1]
                self.hitbox.top = 1

    def player_collision(self, paddle_hitbox : pygame.Rect) -> None:
        '''
        Check collision of player with ball and if it is a side collision teleports ball to prevent 
        ball buggin inside of the paddle
        '''
        self.direction[1] = -self.direction[1]
        # 'If' below is for side hits
        if self.hitbox.bottom - 1 > paddle_hitbox.top: # -1 pixel to prevent side hit happening on every collision
            self.direction[0] = -self.direction[0]
            if self.hitbox.centerx > paddle_hitbox.centerx: # checks side of the hit to teleport it correctly
                self.hitbox.left = paddle_hitbox.right + 2
            else:
                self.hitbox.right = paddle_hitbox.left - 2


    def computer_collision(self, paddle_hitbox : pygame.Rect) -> None:
        '''
        Check collision of computer player with ball and if it is a side collision teleports ball to prevent 
        ball buggin inside of the paddle
        '''
        self.direction[1] = -self.direction[1]
        # 'If' below is for side hits
        if self.hitbox.top + 1 < paddle_hitbox.bottom: # +1 pixel to prevent side hit happening on every collision
            self.direction[0] = -self.direction[0]
            if self.hitbox.centerx > paddle_hitbox.centerx: # checks side of the hit to teleport it correctly
                self.hitbox.left = paddle_hitbox.right + 2
            else:
                self.hitbox.right = paddle_hitbox.left - 2

    def is_out_of_bounds(self) -> bool:
        if self.hitbox.bottom < consts.WINDOW_TOP_SIDE:
            return True
        if self.hitbox.top > consts.WINDOW_HEIGH:
            return True
        return False
    
    def reset(self) -> None:
        self.direction = consts.BALL_INITIAL_DIRECTION
        self.hitbox = pygame.Rect(self.starting_position_rectangle)