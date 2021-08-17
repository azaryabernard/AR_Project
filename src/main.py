import sys
import cv2
import mediapipe
from time import sleep
import sh
import customStyleSheet as cs
import webEngineBrowser as wb
import embed_terminal_1 as et
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QGridLayout
from PyQt5.QtCore import QTimer, QTime, Qt, QSize, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QWindow, QPixmap
import numpy as np
from pynput.mouse import Button, Controller


######################
W_WIDTH = 1920
W_HEIGHT = 1080
S_WIDTH = 960
S_HEIGHT = 540
FRAMER_X = 100
FRAMER_Y = 100
SMOOTHENING = 5
######################


plocX,plocY = 0, 0
clocX, clocY = 0, 0
cur_landmark = (None,None)
mouse = Controller()


#EXPERIMENTAL VIDEO
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        drawingModule = mediapipe.solutions.drawing_utils
        handsModule = mediapipe.solutions.hands

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, S_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, S_HEIGHT)
        with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:

            while self._run_flag:
                ret, frame = cap.read()
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
                                        results.multi_hand_landmarks[0].landmark[12])
                        #4 THUMB, secondary TIP
                        #8 INDEX FINGER TIP
                        #12 MIDDLE

                    #cv2.rectangle( used_image, (FRAMER_X, FRAMER_Y), (S_WIDTH-FRAMER_X, S_HEIGHT-FRAMER_Y), (255,0,255), 2)
                    self.change_pixmap_signal.emit(used_image)
                    
        
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

#END EXPERIMENTAL
        
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AR Prototype 0.1')
        self.resize(W_WIDTH,W_HEIGHT)
        self.setStyleSheet(cs.mainwindow_style);
        self.initVideo()
        self.initUI()
        
        
    def initUI(self):
        self.init_buttons()
        self.init_labels()
        self.webBrowser = QWidget()
        self.webBrowser.setEnabled(False)

        lay = QGridLayout()
        self.setLayout(lay)
        lay.setColumnStretch(0, 1)
        lay.setColumnStretch(1, 1)
        lay.setColumnStretch(2, 1)
        lay.setRowStretch(0, 1)
        lay.setRowStretch(1, 4)
        lay.setRowStretch(2, 1)

        #Timer for updating all widgets
        timer = QTimer(self)
        timer.timeout.connect(self.updateAll)
        timer.start(1000)
    

    def init_buttons(self):
        #EXIT BUTTON
        self.exit_button = QPushButton('X', self)
        self.exit_button.resize(37,37)
        self.exit_button.setStyleSheet(cs.exit_button_style)
        self.exit_button.move(W_WIDTH-45, W_HEIGHT-45)
        self.exit_button.clicked.connect(self.close)
        
        #SIDEBAR BUTTONS
        offsetX = 8
        offsetY = 225
        self.browserBtn = QPushButton(self)
        self.browserBtn.setIcon(QIcon('../image/webBrowserIconGray.png'))
        self.browserBtn.setIconSize(QSize(72, 72))
        self.browserBtn.setStyleSheet(cs.icon_style)
        self.browserBtn.resize(96,96)
        self.browserBtn.move(offsetX, offsetY)
        self.browserBtn.clicked.connect(self.browserBtnClicked)


    def init_labels(self):
        self.time_label = QLabel('', self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.resize(150, 60)
        self.time_label.move(W_WIDTH-158, 8)
        self.time_label.setStyleSheet(cs.time_label_style)

        self.program_log = QLabel('Log: ', self)
        self.program_log.setAlignment(Qt.AlignRight)
        self.program_log.resize(150, 30)
        self.program_log.move(10, W_HEIGHT-50)
        self.program_log.setStyleSheet('color:green; font: 20px; border:0px; ')

    
    def browserBtnClicked(self):
        if not self.webBrowser.isEnabled():
            self.program_log.setText('open browser')
            self.webBrowser = wb.Browser(size=[626, 672])
            self.webBrowser.setEnabled(True)
            self.layout().addWidget(self.webBrowser, 1, 2, 1, 1)
            
        elif not self.webBrowser.isVisible():
            self.program_log.setText("un-minimized browser")
            self.webBrowser.setVisible(True)

        else:
            self.program_log.setText('passed')
            pass
            

    def updateAll(self):
            current_time = QTime.currentTime()
            label_time = current_time.toString('hh:mm:ss')
            self.time_label.setText(label_time)
    
    
    #FOR VIDEO
    def initVideo(self):
        self.image_label = QLabel(self)
        self.image_label.resize(S_WIDTH, S_HEIGHT)
        self.image_label.move((W_WIDTH-S_WIDTH)/2, (W_HEIGHT-S_HEIGHT)/2)
        self.border_label = QLabel(self)
        self.border_label.resize(S_WIDTH - 2*FRAMER_X, S_HEIGHT - 2*FRAMER_Y)
        self.border_label.move((W_WIDTH-S_WIDTH)/2 + FRAMER_X, (W_HEIGHT-S_HEIGHT)/2 + FRAMER_Y)
        self.border_label.setStyleSheet("background-color: none; border-image: none; border-width: 2px; border-color: pink;")
        
         # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
    
    
    def closeEvent(self, event):
        self.thread.stop()
        event.accept()
        
        
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        global plocX
        global plocY
        global clocX
        global clocY
        global cur_landmark

        #Updates the image_label with a new opencv image
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        #print(cur_landmark)
        if cur_landmark != (None, None): 
            #convert coordinates
            (index_x, index_y) = (np.interp(cur_landmark[0].x * S_WIDTH, (FRAMER_X, S_WIDTH-FRAMER_X), (0, W_WIDTH)), 
                                    np.interp(cur_landmark[0].y * S_HEIGHT, (FRAMER_Y, S_HEIGHT-FRAMER_Y), (0, W_HEIGHT)))
            
            
            (secondary_x, secondary_y) = (np.interp(cur_landmark[1].x * S_WIDTH, (FRAMER_X, S_WIDTH-FRAMER_X), (0, W_WIDTH)), 
                                            np.interp(cur_landmark[1].y * S_HEIGHT, (FRAMER_Y, S_HEIGHT-FRAMER_Y), (0, W_HEIGHT)))

            #smoothening
            clocX = plocX + (index_x - plocX) / SMOOTHENING
            clocY = plocY + (index_y - plocY) / SMOOTHENING
            
            #mouse events
            mouse.position = (clocX, clocY)
            secondary_index_sq = (secondary_x - index_x)**2 + (secondary_y - index_y)**2

            if( secondary_index_sq <= 11000 and secondary_index_sq >= 5000):
                mouse.click(Button.left, 1)
                self.program_log.setText("click!")
            else:
                self.program_log.setText("not click")
            
            plocX, plocY = clocX, clocY
            cur_landmark = (None, None)
            
    
    def convert_cv_qt(self, cv_img):
        #Convert from an opencv image to QPixmap
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(cv_img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(S_WIDTH, S_HEIGHT, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    #END FOR VIDEO

    
    def experimental(self):
        et.Container()
        sleep(3)
        winid = int([l for l in sh.xwininfo('-root', '-tree').split('\n') if "Mozilla Firefox" in l][0].split('"Mozilla Firefox"')[0].strip(), 16)
        testWindow = QWindow.fromWinId(winid)
        testWindow.setFlags(Qt.FramelessWindowHint)
        testWindow.resize(300,300)
        self.testWidgetFromWindow = QWidget.createWindowContainer(testWindow)
        self.testWidgetFromWindow.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.testWidgetFromWindow.setStyleSheet("background-color: white;")
        self.layout().addWidget(self.testWidgetFromWindow)


def main(): 
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.showFullScreen()

    sys.exit(app.exec_())
        


if __name__ == '__main__':
    main()