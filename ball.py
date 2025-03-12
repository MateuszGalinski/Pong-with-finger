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
        self.direction = consts.BALL_INITIAL_DIRECTION  # format [x,y] where -1 <= x,y <= 1
        self.collision_counter = 0
        self.in_collision = False

    def draw(self, surface : pygame.SurfaceType) -> None:
        pygame.draw.circle(surface, self.color, (self.hitbox.centerx, self.hitbox.centery), consts.BALL_RADIUS)

    def move(self) -> None:
        self.hitbox.centerx = self.hitbox.centerx + self.direction[0] * consts.BALL_SPEED
        self.hitbox.centery = self.hitbox.centery + self.direction[1] * consts.BALL_SPEED

    def check_colision(self, paddle: Paddle, bounce_off_top_edge: bool = False) -> bool:
        if self.hitbox.right >= consts.WINDOW_WIDTH:
            self.direction[0] = -self.direction[0]
            self.hitbox.right = consts.WINDOW_WIDTH - 1

        if self.hitbox.left <= consts.WINDOW_LEFT_SIDE:
            self.direction[0] = -self.direction[0]
            self.hitbox.left = consts.WINDOW_SAFE_ZONE_LEFT

        paddle_hitbox = paddle.get_hitbox()

        # print("PADDLE TOP: " + str(paddle_hitbox.top))
        # print("BALL HITBOX CENTERY")

        if self.hitbox.colliderect(paddle_hitbox):
            if not self.in_collision:
                self.in_collision = True
                if paddle.is_human:
                    self.player_collision(paddle_hitbox)
                else:
                    self.computer_collision(paddle_hitbox)
                self.collision_counter += 1
                paddle.points += 1
                if self.collision_counter % 3 == 0:
                    consts.BALL_SPEED = min(consts.MAX_BALL_SPEED, consts.BALL_SPEED + 0.1)
                    print(consts.BALL_SPEED)
            return True
        else:
            self.in_collision = False

        if bounce_off_top_edge:
            if self.hitbox.top < 0:
                self.direction[1] = -self.direction[1]
                self.hitbox.top = 1
        return False

    def player_collision(self, paddle_hitbox : pygame.Rect) -> None:
        '''
        Check collision of player with ball and if it is a side collision teleports ball to prevent 
        ball buggin inside of the paddle
        '''
        self.direction[1] = -1
        self.hitbox.bottom = paddle_hitbox.top
        if self.hitbox.centerx < paddle_hitbox.left or self.hitbox.centerx > paddle_hitbox.right:
            self.direction[0] = -self.direction[0]
        self.hitbox.bottom = paddle_hitbox.top - 1


    def computer_collision(self, paddle_hitbox : pygame.Rect) -> None:
        '''
        Check collision of computer player with ball and if it is a side collision teleports ball to prevent 
        ball buggin inside of the paddle
        '''
        self.direction[1] = 1
        self.hitbox.top = paddle_hitbox.bottom
        if self.hitbox.centerx < paddle_hitbox.left or self.hitbox.centerx > paddle_hitbox.right:
            self.direction[0] = -self.direction[0]
        self.hitbox.top = paddle_hitbox.bottom + 1

    def is_out_of_bounds(self) -> bool:
        if self.hitbox.bottom < consts.WINDOW_TOP_SIDE:
            return True
        if self.hitbox.top > consts.WINDOW_HEIGH:
            return True
        return False
    
    def reset(self) -> None:
        self.direction = consts.BALL_INITIAL_DIRECTION
        self.hitbox = pygame.Rect(self.starting_position_rectangle)
        self.collision_counter = 0
        self.in_collision = False
        consts.BALL_SPEED = 1
