import numpy as np
import random
import consts
from paddle import Paddle


def normalize(value, center, min_value, max_value):
    return (value - center)/(max_value - min_value)


class QValuePaddle(Paddle):
    def __init__(self, x_corner : int, y_corner : int, color : str = '#FFFFFF', test=False):
        super().__init__(x_corner, y_corner, color=color, is_human=False)
        self.actions = ["left", "right", "stop"]
        self.alpha = 0.01
        self.epsilon = 0.99
        self.gamma = 0.7

        self.last_action = 'stop'
        self.num_features = 9
        self.weights = np.ones(self.num_features)
        if test:
            self.load_weights()
            self.turn_off_learning()
        self.total_reward = 0

    def choose_action(self, state):
        return self.get_action(state)

    def get_features(self, state, action):
        ball, player, opponent, block = state
        ball_x, ball_y = ball[0].center
        ball_dir = ball[1]
        ball_speed = ball[2]
        player_x, player_y = player.center
        opponent_x, _ = opponent.center
        block_x, block_y = block.center

        if action == "left":
            projected_player_x = max(player_x - consts.PADDLE_SPEED, 0)
        elif action == "right":
            projected_player_x = min(player_x + consts.PADDLE_SPEED, consts.WINDOW_WIDTH)
        else:
            projected_player_x = player_x

        features = [1.0]

        features.extend([
            normalize(ball_x, projected_player_x, 0, consts.WINDOW_WIDTH),
            normalize(ball_y, player_y, 0, consts.WINDOW_HEIGH),
            ball_dir[0], ball_dir[1],
            normalize(ball_speed, (consts.MIN_BALL_SPEED + consts.MAX_BALL_SPEED)/2,
                      consts.MIN_BALL_SPEED, consts.MAX_BALL_SPEED),
            normalize(block_x, projected_player_x, 0, consts.WINDOW_WIDTH),
            normalize(block_y, player_y, 0, consts.WINDOW_HEIGH),
            normalize(opponent_x, projected_player_x, 0, consts.WINDOW_WIDTH)
        ])

        # print('features', features)
        return np.array(features)

    def update(self, state, action, reward, next_state):
        if next_state is None:
            target = reward
        else:
            next_action = max(self.actions, key=lambda a: self.get_q_value(next_state, a))
            target = reward + self.gamma * self.get_q_value(next_state, next_action)

        td_error = target - self.get_q_value(state, action)
        features = self.get_features(state, action)
        # print('lambda',self.alpha * td_error * features)
        self.weights += self.alpha * td_error * features
        self.total_reward += reward

    def get_q_value(self, state, action):
        features = self.get_features(state, action)
        # print('q_values', np.dot(features, self.weights))
        return np.dot(features, self.weights)

    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            q_values = [self.get_q_value(state, action) for action in self.actions]
            return self.actions[np.argmax(q_values)]

    def turn_off_learning(self):
        self.epsilon = 0
        self.alpha = 0

    def save_weights(self, filename='weights.txt'):
        np.savetxt(filename, self.weights)

    def load_weights(self, filename='weights.txt'):
        self.weights = np.loadtxt(filename)
