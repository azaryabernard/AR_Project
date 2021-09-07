import cv2
import mediapipe as mp
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread
from _config import *

cur_landmark = (None,None)

#EXPERIMENTAL VIDEO
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        drawingModule = mp.solutions.drawing_utils
        handsModule = mp.solutions.hands

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, S_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, S_HEIGHT)
        with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:

            while self._run_flag:
                self.sleep(0.1)
                ret, frame = cap.read()
                if not ret:
                    continue
                
                flipped = cv2.flip(frame, flipCode = -1)
                
                results = hands.process(cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB))
                   
                blank_image = np.zeros(shape=[S_HEIGHT, S_WIDTH, 3], dtype=np.uint8)
                used_image = blank_image

                #DRAWING THE HAND CONNECTION
                if results.multi_hand_landmarks != None:
                    for handLandmarks in results.multi_hand_landmarks:
                        drawingModule.draw_landmarks(used_image, handLandmarks, handsModule.HAND_CONNECTIONS)
          
                if ret:
                    if results.multi_hand_landmarks:
                        global cur_landmark
                        cur_landmark = (results.multi_hand_landmarks[0].landmark[8], 
                                        results.multi_hand_landmarks[0].landmark[12],
                                        results.multi_hand_landmarks[0].landmark[20])
                        #4 THUMB, secondary TIP
                        #8 INDEX FINGER TIP
                        #6 first join index
                        #12 MIDDLE

                    #cv2.rectangle( used_image, (FRAMER_X, FRAMER_Y), (S_WIDTH-FRAMER_X, S_HEIGHT-FRAMER_Y), (255,0,255), 2)
                    self.change_pixmap_signal.emit(used_image)
                    
        
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
#END EXPERIMENTAL

