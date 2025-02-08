import cv2
import mediapipe as mp
import os

class HandDetector:
    BaseOptions = mp.tasks.BaseOptions
    HandLandmaarker = mp.tasks.vision.HandLandmarker
    HandLandmaarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    HandLandmaarkerResult = mp.tasks.vision.HandLandmarkerResult
    VisionRunningMode = mp.tasks.vision.RunningMode

    def __init__(self, callback):
        # self.camera = cv2.VideoCapture(0)
        self.timestamp = 0
        model_path = os.path.join("hand_landmarker.task" )
        base_options = self.BaseOptions(model_asset_path=model_path)
        running_mode = self.VisionRunningMode.LIVE_STREAM

        options = self.HandLandmaarkerOptions(base_options = base_options,
                                                num_hands = 2   ,
                                                running_mode = running_mode,
                                                result_callback = callback)
        
        self.detector = self.HandLandmaarker.create_from_options(options)

        self.video = cv2.VideoCapture(0)

    def process_finger_data(self):
        if self.video.isOpened():
            ret, frame = self.video.read()

            if not ret:
                print("Ignoring empty frame")
                return

            self.timestamp += 1
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            self.detector.detect_async(mp_image, self.timestamp)

    def calculate_results(self, image : mp.Image, timestamp_ms : int):
        self.detector.detect_async(image, timestamp_ms)

    def close(self):
        self.video.release()

def print_result(result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    hand_landmarks_list = result.hand_landmarks
    print(type(hand_landmarks_list))
    if(len(hand_landmarks_list)>0):
        hand_landmarks = hand_landmarks_list[0]
        print ('finger position: {}'.format(hand_landmarks[8]))

def test2():
    h_detector = HandDetector(print_result)

    while True:
        h_detector.process_finger_data()

if __name__ == "__main__":
    test2()