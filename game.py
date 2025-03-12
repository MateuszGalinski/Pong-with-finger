import pygame
import consts
from paddle import Paddle
from ball import Ball
from cursor import Cursor
from handdetector import HandDetector
from block import Block
import threading
import time

class Game:
    def __init__(self, caption: str = 'Pong', background_color: str = "#000000"):
        pygame.init()
        pygame.display.set_caption(caption)
        self.window_surface = pygame.display.set_mode((consts.WINDOW_WIDTH, consts.WINDOW_HEIGH))

        self.background = pygame.Surface((consts.WINDOW_WIDTH, consts.WINDOW_HEIGH))
        self.background.fill(pygame.Color(background_color))

        human_player = Paddle(consts.PLAYER_STARTING_POSITION[0], consts.PLAYER_STARTING_POSITION[1])
        bot_player = Paddle(consts.COMPUTER_STARTING_POSITION[0], consts.COMPUTER_STARTING_POSITION[1], is_human=False)
        self.players = [human_player, bot_player]
        self.ball = Ball()
        self.cursor = Cursor()
        self.block = Block()

        self.hand_detector = HandDetector(self.cursor.follow_finger)
        self.drawables = [human_player, bot_player, self.ball, self.cursor, self.block]
        self.running = True
        self.last_player_touched = None

        self.finger_thread = threading.Thread(target=self.process_finger_data)
        self.finger_thread.daemon = True  # Allow the thread to exit when the main program exits
        self.finger_thread.start()

    def game_frame(self) -> None:
        self.window_surface.blit(self.background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        for player in self.players:
            if player.is_human:
                player.move_to_cursor(self.cursor)
            else:
                self.move_bot_paddle(player)
            if self.ball.check_colision(player, bounce_off_top_edge=False):
                self.last_player_touched = player
                self.block.active = True

        self.ball.move()

        if self.block.check_collision(self.ball.hitbox, self.last_player_touched):
            self.block.reset()

        for item in self.drawables:
            item.draw(self.window_surface)

        self.draw_points()

        if self.ball.is_out_of_bounds():
            self.reset()
            # self.end_game()

        pygame.display.update()

    def move_bot_paddle(self, bot_paddle: Paddle):
        if bot_paddle.hitbox.centerx < self.ball.hitbox.centerx:
            bot_paddle.move_right()
        elif bot_paddle.hitbox.centerx > self.ball.hitbox.centerx:
            bot_paddle.move_left()

    def draw_points(self):
        font = pygame.font.Font(None, 36)
        human_points_text = font.render(f"Player: {self.players[0].points}", True, (255, 255, 255))
        bot_points_text = font.render(f"Bot: {self.players[1].points}", True, (255, 255, 255))
        self.window_surface.blit(human_points_text, (50, consts.WINDOW_HEIGH - 50))
        self.window_surface.blit(bot_points_text, (50, 50))

    def is_running(self) -> bool:
        return self.running

    def reset(self):
        print("RESET")
        for player in self.players:
            player.reset()
        self.ball.reset()
        self.block.reset()

    def end_game(self):
        print("GAME OVER")
        self.running = False
        self.show_final_scores()

    def show_final_scores(self):
        font = pygame.font.Font(None, 72)
        final_text = font.render(f"Final Scores - Player: {self.players[0].points}  Bot: {self.players[1].points}", True, (255, 255, 255))
        text_rect = final_text.get_rect(center=(consts.WINDOW_WIDTH / 2, consts.WINDOW_HEIGH / 2))
        self.window_surface.blit(final_text, text_rect)
        pygame.display.update()
        pygame.time.wait(10000)

    def end(self):
        self.hand_detector.close()

    def process_finger_data(self):
        while self.running:
            self.hand_detector.process_finger_data()

            # Small delay to prevent the processing from taking too much CPU time
            time.sleep(consts.DELAY_BETWEEN_FINGER_DETECTION)
