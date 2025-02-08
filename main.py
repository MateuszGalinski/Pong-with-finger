import pygame
import consts
from paddle import Paddle
from ball import Ball
from game import Game

def main():
    game = Game()
    clock = pygame.time.Clock()

    while game.is_running():
        game.game_frame()
        clock.tick(consts.FRAMERATE)
    
    game.end()

if __name__ == "__main__":
    main()