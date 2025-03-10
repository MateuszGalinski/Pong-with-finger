import consts
import pygame
import mediapipe as mp

class Cursor:
    def __init__(self, color : str = "#3832a8"):
        x_center = consts.WINDOW_WIDTH/2
        y_center = consts.WINDOW_HEIGH/2
        self.hitbox = pygame.Rect(x_center - consts.BALL_RADIUS, 
                                  y_center - consts.BALL_RADIUS, 
                                  consts.CURSOR_RADIUS * 2, 
                                  consts.CURSOR_RADIUS * 2)
        self.color = color
        pass

    def draw(self, surface : pygame.SurfaceType) -> None:
        pygame.draw.ellipse(surface,
                            self.color,
                            self.hitbox,
                            consts.CURSOR_WIDTH)

    def follow_finger(self, result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        hand_landmarks_list = result.hand_landmarks
        if(len(hand_landmarks_list)>0):
            hand_landmarks = hand_landmarks_list[0]
            pointing_finger_location = hand_landmarks[8]
            # print("Y LOCATION OF A FINGER: " + str(pointing_finger_location.y))
            self.hitbox.x = (1 - pointing_finger_location.x) * consts.WINDOW_WIDTH #deleting X from one to flip an image in more optimal way
            self.hitbox.y = pointing_finger_location.y * consts.WINDOW_HEIGH
            

    def set_position(self, position):
        pass

    def get_hitbox(self):
        return self.hitbox