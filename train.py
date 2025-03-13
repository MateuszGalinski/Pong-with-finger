import numpy as np
import pygame
import consts
from paddle import Paddle
from ball import Ball
from block import Block
from qlearning_agent import QValuePaddle


class TrainingGame:
    def __init__(self, caption: str = 'Pong Training', background_color: str = "#000000"):
        self.q_agent = QValuePaddle(consts.COMPUTER_STARTING_POSITION[0], consts.COMPUTER_STARTING_POSITION[1], test=False)
        self.q_bot = QValuePaddle(consts.PLAYER_STARTING_POSITION[0], consts.PLAYER_STARTING_POSITION[1], test=False)
        self.players = [self.q_bot, self.q_agent]
        self.ball = Ball()
        self.block = Block()

        self.running = True
        self.last_player_touched = None

    def get_state(self):
        return [self.ball.hitbox, self.ball.direction, self.ball.speed], self.players[1].hitbox, self.players[
            0].hitbox, self.block.hitbox

    def game_frame(self) -> int:
        for player in self.players:
            if isinstance(player, QValuePaddle):
                state = self.get_state()
                action = player.get_action(state)
                if action == "left":
                    player.move_left()
                elif action == "right":
                    player.move_right()
            if self.ball.check_colision(player, bounce_off_top_edge=False):
                self.last_player_touched = player
                self.block.active = True

        self.ball.move()

        if self.block.check_collision(self.ball.hitbox, self.last_player_touched):
            self.block.reset()

        if self.ball.is_out_of_bounds():
            return 1 if self.last_player_touched == self.q_agent else 2
        return 0

    def move_bot_paddle(self, bot_paddle: Paddle):
        if bot_paddle.hitbox.centerx < self.ball.hitbox.centerx:
            bot_paddle.move_right()
        elif bot_paddle.hitbox.centerx > self.ball.hitbox.centerx:
            bot_paddle.move_left()

    def is_running(self) -> bool:
        return self.running

    def reset(self):
        print("RESET")
        for player in self.players:
            player.reset()
        self.ball.reset()
        self.block.reset()

def train_agent():
    game = TrainingGame()
    episodes = 100000
    limit_episode_len = 10000
    best_reward = -np.inf

    for episode in range(episodes):
        game.reset()
        state = game.get_state()
        while game.is_running() and limit_episode_len > 0:
            result = game.game_frame()
            if result:
                reward = -50 if result == 1 else 50
                game.q_agent.update(state, game.q_agent.last_action, reward, None)
                game.q_bot.update(state, game.q_bot.last_action, -reward, None)  # Opposite reward for the opponent
                break

            next_state = game.get_state()
            reward_agent = calculate_reward(state, game.q_agent.last_action, next_state)
            reward_bot = calculate_reward(state, game.q_bot.last_action, next_state)

            game.q_agent.update(state, game.q_agent.last_action, reward_agent, next_state)
            game.q_bot.update(state, game.q_bot.last_action, reward_bot, next_state)

            state = next_state
            limit_episode_len -= 1

        episode_reward = game.q_agent.total_reward
        print(f"Episode {episode + 1} completed. Total reward: {episode_reward}")
        if episode_reward > best_reward:
            best_reward = episode_reward
            game.q_agent.save_weights(f'best.txt')
        game.q_agent.save_weights()
        game.q_agent.epsilon = max(0.1, game.q_agent.epsilon * 0.999)
        game.q_agent.alpha = max(0.001, game.q_agent.alpha * 0.999)
        game.q_bot.epsilon = max(0.1, game.q_bot.epsilon * 0.999)
        game.q_bot.alpha = max(0.001, game.q_bot.alpha * 0.999)
        limit_episode_len = 1000000


def calculate_reward(prev_state, action, current_state):
    ball_prev = prev_state[0]
    ball_current = current_state[0]
    player_prev = prev_state[1]
    player_current = current_state[1]
    block_prev = prev_state[3]
    block_current = current_state[3]

    ball_current_dir = ball_current[1]
    ball_prev_dir = ball_prev[1]

    reward = 1

    if ball_prev_dir[1] < 0 < ball_current_dir[1]:
        reward += 15

    if ball_current[0].top < player_current.centery:
        reward -= 5

    if block_prev.center != block_current.center and ball_current_dir[1] < 0:
        reward += 20

    ball_x, _ = ball_current[0].center
    player_x, _ = player_current.center
    distance_to_ball = abs(ball_x - player_x)
    reward += (consts.WINDOW_WIDTH - distance_to_ball) / consts.WINDOW_WIDTH * 0.5


    if action == "left" and ball_x > player_x:
        reward -= 1
    elif action == "right" and ball_x < player_x:
        reward -= 1

    return reward


if __name__ == "__main__":
    train_agent()
