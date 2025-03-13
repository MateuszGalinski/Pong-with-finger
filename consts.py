from pygame import K_RIGHT, K_LEFT, K_a, K_d

FRAMERATE = 240 #frames per seconds
DELAY_BETWEEN_FINGER_DETECTION = 0.1 # in seconds

WINDOW_WIDTH = 800
WINDOW_HEIGH = 1000
WINDOW_TOP_SIDE = 0
WINDOW_LEFT_SIDE = 0
WINDOW_SAFE_ZONE_LEFT = 1

PADDLE_SPEED = 2 # pixels per frame
PADDLE_WIDTH = WINDOW_WIDTH * 0.2
PADDLE_LENGTH = WINDOW_HEIGH * 0.05

BALL_RADIUS = WINDOW_WIDTH * 0.02
MIN_BALL_SPEED = 0.8 # pixels per frame
MAX_BALL_SPEED = 4
BALL_INITIAL_DIRECTION = [-1,1]

CURSOR_RADIUS = 10
CURSOR_WIDTH = 2

HUMAN_PLAYER_CONTROLS = {"left" : K_LEFT, 
                         "right": K_RIGHT}
PLAYER_STARTING_POSITION = (0.1 * WINDOW_WIDTH, 0.9 * WINDOW_HEIGH)

COMPUTER_PLAYER_CONTROLS = {"left" : K_a, 
                            "right" : K_d}
COMPUTER_STARTING_POSITION = (0.1 * WINDOW_WIDTH, 0.1 * WINDOW_HEIGH)

BLOCK_WIDTH = WINDOW_WIDTH * 0.7
BLOCK_HEIGHT = WINDOW_HEIGH * 0.05
BLOCK_POINTS = 5
