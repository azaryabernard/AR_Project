import mediapipe
import numpy as np
import cv2


drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:

     while True:
           ret, frame = cap.read()
           flipped = cv2.flip(frame, flipCode = -1)
           frame1 = cv2.resize(flipped, (640, 480))
           results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
           
           blank_image = np.zeros(shape=[480, 640, 3], dtype=np.uint8)
           
           if results.multi_hand_landmarks != None:
              for handLandmarks in results.multi_hand_landmarks:
                  drawingModule.draw_landmarks(blank_image, handLandmarks, handsModule.HAND_CONNECTIONS)
  
           cv2.imshow("Frame", blank_image);
           key = cv2.waitKey(1) & 0xFF
           if key == ord("q") or cv2.getWindowProperty("Frame", 1) < 1:
              break
