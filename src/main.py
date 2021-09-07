import sys
import sh
import os
import numpy as np
import handtracking as ht
import customStyleSheet as cs
import webEngineBrowser as wb
import embedded_app as embed
from math import hypot
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QGridLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt, QSize, pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap, QWindow, QImage, QBrush, QPalette
from pynput.mouse import Button, Controller
from RPi import GPIO
from _config import *
import speechrecognition
from time import sleep



######################
MOUSE = Controller()
MOUSE_TRACKABLE = True
APP_POS = [2,1,3]
PCIDS = []
plocX,plocY = 0, 0
clocX, clocY = 0, 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(MIC_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(HT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
old_time = QTime.currentTime()
self_timer = False
mutex1 = True
######################
        
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AR Prototype 0.1')
        self.resize(W_WIDTH, W_HEIGHT)
        self.ht_thread = None
        self.initUI()
        
        
    def initUI(self):
        oImage = QImage("../image/backgroundV2.png")
        sImage = oImage.scaled(QSize(W_WIDTH, W_HEIGHT))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        lay = QGridLayout(self)
        lay.setColumnStretch(0, 4)
        lay.setColumnStretch(1, 3)
        lay.setColumnStretch(2, 4)
        lay.setRowStretch(0, 1)
        lay.setRowStretch(1, 2)
        lay.setRowStretch(2, 2)
        lay.setRowStretch(3, 1)
        lay.setContentsMargins(15, 15, 15, 50)
        self.setLayout(lay)
        
        self.init_buttons()
        self.init_labels()
        self.webBrowser = None
        self.embeddedApp1 = None
        self.embeddedApp2 = None

        #Timer for updating all widgets
        timer = QTimer(self)
        timer.timeout.connect(self.updateAll)
        timer.start(1000)
    

    def init_buttons(self):
        self.dummyBtn = QPushButton(self)
        self.dummyBtn.resize(0, 0)
        #EXIT BUTTON
        self.powerBtn = QPushButton(self)
        self.powerBtn.setIcon(QIcon('../image/powerIcon.png'))
        self.powerBtn.resize(70,70)
        self.powerBtn.setStyleSheet(cs.smallIcon_style)
        self.powerBtn.move(W_WIDTH-100, 40)
        self.powerBtn.clicked.connect(self.close)
        
        #MIC BUTTON
        self.micBtn = QPushButton(self)
        self.micBtn.setIcon(QIcon('../image/microphoneIcon.png'))
        self.micBtn.resize(70,70)
        self.micBtn.setStyleSheet(cs.smallIcon_style)
        self.micBtn.move(30, 40)
        self.micBtn.clicked.connect(self.startMIC)
        
        #SIDEBAR BUTTONS
        self.browserBtn = QPushButton(self)
        self.browserBtn.setIcon(QIcon('../image/webBrowserIcon.png'))
        self.browserBtn.setStyleSheet(cs.icon_style)
        self.browserBtn.clicked.connect(self.browserBtnClicked)

        self.youtubeBtn = QPushButton(self)
        self.youtubeBtn.setIcon(QIcon('../image/youtubeIcon.png'))
        self.youtubeBtn.setStyleSheet(cs.icon_style)
        self.youtubeBtn.clicked.connect(lambda state, appname='YouTube', args=["--profile-directory=Default", "--app-id=agimnkijcaahngcdmfeangaknmldooml"]: self.embed_app1(appname, args)) #--profile-directory=Default", "--app-id=agimnkijcaahngcdmfeangaknmldooml
        
        self.terminalBtn = QPushButton(self)
        self.terminalBtn.setIcon(QIcon('../image/terminalIcon.png'))
        self.terminalBtn.setStyleSheet(cs.icon_style)
        self.terminalBtn.clicked.connect(lambda state, appname='lxterminal', args=["--working-directory=/home/pi/Desktop"]: self.embed_app2(appname, args))
        
        self.handTrackingBtn = QPushButton(self)
        self.handTrackingBtn.setIcon(QIcon('../image/handIcon.png'))
        self.handTrackingBtn.setStyleSheet(cs.icon_style)
        self.handTrackingBtn.clicked.connect(self.initVideo)
        
        
        horLayout = QHBoxLayout()
        horLayout.addStretch()
        horLayout.addWidget(self.browserBtn)
        horLayout.addWidget(self.youtubeBtn)
        horLayout.addWidget(self.terminalBtn)
        horLayout.addWidget(self.handTrackingBtn)
        horLayout.setSpacing(10)
        horLayout.addStretch()
        self.layout().addLayout(horLayout, 3, 0, 1, 3)
        


    def init_labels(self):
        self.time_label = QLabel('', self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.resize(150, 60)
        self.time_label.move( (W_WIDTH-150) / 2, 42)
        self.time_label.setStyleSheet(cs.time_label_style)

        self.speech_label = QLabel('', self)
        self.speech_label.setAlignment(Qt.AlignCenter)
        self.speech_label.resize(400, 60)
        self.speech_label.move( (W_WIDTH-400) / 2, W_HEIGHT / 2 + 100)
        self.speech_label.setStyleSheet(cs.speech_label_style)

        self.program_log = QLabel('Log: ', self)
        self.program_log.setAlignment(Qt.AlignLeft)
        self.program_log.resize(300, 35)
        self.program_log.move(10, W_HEIGHT-50)
        self.program_log.setStyleSheet(cs.log_style)

        frameX = S_WIDTH / 2
        frameY = S_HEIGHT / 2
        self.image_label = QLabel(self)
        self.image_label.resize(frameX, frameY)
        self.image_label.setStyleSheet(cs.ht_border_style)
        self.border_label = QLabel(self)
        self.border_label.resize(frameX - FRAMER_X, frameY - FRAMER_Y)
        self.border_label.setStyleSheet(cs.ht_border_style) 
        self.border_label.setVisible(False)
        self.image_label.setVisible(False)
        self.image_label.move((W_WIDTH-frameX)/2, (W_HEIGHT-frameY)/2 - 200)
        self.border_label.move((W_WIDTH-frameX)/2 + FRAMER_X/2, (W_HEIGHT-frameY)/2 + FRAMER_Y/2 - 200)

    def embed_app1(self, appname, args):
        browserSize = [450, 550]
        if not self.embeddedApp1 or not self.embeddedApp1.isEnabled():
            self.program_log.setText('open browser')
            self.embeddedApp1 = wb.Browser(size=browserSize, default_url='https://www.youtube.com', style=1)
            self.embeddedApp1.setEnabled(True)
            self.layout().addWidget(self.embeddedApp1, 1, 2, 2, 1)
            
        elif not self.embeddedApp1.isVisible() and self.embeddedApp1.isEnabled():
            self.program_log.setText("maximized browser")
            self.embeddedApp1.setVisible(True)

        else:
            self.program_log.setText('passed')
      
    def embed_app2(self, appname, args):
        if not self.embeddedApp2 or not self.embeddedApp2.isEnabled():
            self.embeddedApp2 = embed.EmbeddedApp(appname, args)
            if not self.embeddedApp2:
                self.program_log.setText("App not opened!")
                return
            
            global PCIDS
            PCIDS.append(self.embeddedApp2.pcid)
            
            self.program_log.setText("App opened")
            self.layout().addWidget(self.embeddedApp2, 2, 1, 1, 1)
                
        elif not self.embeddedApp2.isVisible() and self.embeddedApp2.isEnabled():
            self.program_log.setText("maximized embedApp")
            self.embeddedApp2.setVisible(True)
        else:
            self.program_log.setText('passed')
        if HANDTRACKED:
            self.closeHand()
            self.initVideo()
        
        
        
    def browserBtnClicked(self):
        browserSize = [450, 550]
            
        if not self.webBrowser or not self.webBrowser.isEnabled():
            self.program_log.setText('open browser')
            self.webBrowser = wb.Browser(size=browserSize)
            self.webBrowser.setEnabled(True)
            self.layout().addWidget(self.webBrowser, 1, 0, 2, 1)
            
        elif not self.webBrowser.isVisible() and self.webBrowser.isEnabled():
            self.program_log.setText("maximized browser")
            self.webBrowser.setVisible(True)

        else:
            self.program_log.setText('passed')
        

    def updateAll(self):
        global MOUSE_CLICKABLE
        global MOUSE_TRACKABLE
        global mutex1
        global self_timer
        global old_time
        MOUSE_CLICKABLE = True
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.time_label.setText(label_time)
        
        if self_timer and old_time.msecsTo(QTime.currentTime()) > 2500:
            self_timer = False
            self.speech_label.clear()
            if not mutex1 and not self.embeddedApp2.isVisible():
                self.embeddedApp2.setVisible(True)
                mutex1 = True
            
        if not GPIO.input(MIC_PIN) and (not self.ht_thread or self.ht_thread and not self.ht_thread.isRunning()) :
            self.startMIC()
            
            
    def startMIC(self):
        global MOUSE_TRACKABLE
        global mutex1
        MOUSE_TRACKABLE = False
        if self.embeddedApp2 and mutex1 and self.embeddedApp2.isVisible():
            self.embeddedApp2.setVisible(False)
            mutex1 = False
        
        self.micBtn.disconnect()
        self.program_log.setText('Listening...')
        self.speech_label.setText('Listening...')
        self.ht_thread = speechrecognition.ListenThread()
        self.ht_thread.command_signal.connect(self.processCommand)
        self.ht_thread.start()
            
    @pyqtSlot(int, str)       
    def processCommand(self, cmd, speech=""):
        global MOUSE_TRACKABLE
        global self_timer
        global old_time
        
        print('processing command: {}'.format(cmd))
        
        if speech:
            self.speech_label.setText(speech)
        else:
            self.speech_label.setText("Oops! Didn't catch that...")
        
        self_timer = True
        old_time = QTime.currentTime()
        
        
        if cmd == -1:
            self.program_log.setText('nothing specified')
        elif cmd == -2:
            self.program_log.setText('no call command!')
        elif cmd == 0:
            self.program_log.setText('command called!')
        elif cmd == 1 and not HANDTRACKED:
            self.handTrackingBtn.animateClick()
        elif cmd == 2 and HANDTRACKED:
            self.handTrackingBtn.animateClick()
        elif cmd == 3:
            self.powerBtn.animateClick()
        try:
            if cmd >= 0:
                sh.cvlc('--play-and-exit', '../sound/sr_processed.m4a')
            else:
                sh.cvlc('--play-and-exit', '../sound/sr_done.m4a')
        except:
            print('error playing sound')
            
        MOUSE_TRACKABLE = True
        self.micBtn.clicked.connect(self.startMIC)
        if HANDTRACKED:
            self.closeHand()
            self.initVideo()
        self.ht_thread.stop()
    
    
    #FOR VIDEO
    def initVideo(self):
        global HANDTRACKED
        
        self.image_label.setVisible(True)
        self.border_label.setVisible(True)
        #print("clicked from: {}", HANDTRACKED)
#         frameX = S_WIDTH / 2
#         frameY = S_HEIGHT / 2
#         self.image_label.move((W_WIDTH-frameX)/2, (W_HEIGHT-frameY)/2 - 200)
#         self.border_label.move((W_WIDTH-frameX)/2 + FRAMER_X/2, (W_HEIGHT-frameY)/2 + FRAMER_Y/2 - 200)
#         
#         if(not self.embeddedApp1 or not self.embeddedApp1.isEnabled() or not self.embeddedApp1.isVisible() ):
#             pass
#         else:
#             self.border_label.move(self.border_label.x() + 40, self.border_label.y())
#             self.image_label.move(self.image_label.x() + 40, self.image_label.y())

        HANDTRACKED = True
        self.handTrackingBtn.disconnect()
        self.handTrackingBtn.clicked.connect(self.closeHand)
        
        # create the video capture thread,  connect its signal to the update_image, start
        self.thread = ht.VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        
        
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        global plocX
        global plocY
        global clocX
        global clocY
        global MOUSE_CLICKABLE
        global MOUSE_TRACKABLE
        OFFSET_X1 = 0
        OFFSET_Y1 = 360

        #Updates the image_label with a new opencv image
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        
        if not MOUSE_TRACKABLE:
            return
        #print(cur_landmark)
        if ht.cur_landmark != (None, None):   
            #self.program_log.setText(str(hypot(ht.cur_landmark[2].x - ht.cur_landmark[0].x, ht.cur_landmark[2].y - ht.cur_landmark[0].y)))
            length = hypot(ht.cur_landmark[1].x - ht.cur_landmark[0].x, ht.cur_landmark[1].y - ht.cur_landmark[0].y)
            #self.program_log.setText(str(length))
            #mouse events
            #print(str("middle y: {}, pinky y: {}".format(ht.cur_landmark[1].y, ht.cur_landmark[2].y)))
#             if length >= 0.16 and length < 0.2:
#                 self.startMIC()
#                 return
            if length >= 0.2:
                #convert coordinates
                (index_x, index_y) = (OFFSET_X1+1280 + np.interp(ht.cur_landmark[0].x * S_WIDTH, (FRAMER_X, S_WIDTH-FRAMER_X), (0, W_WIDTH)), 
                                         OFFSET_Y1 + np.interp(ht.cur_landmark[0].y * S_HEIGHT, (FRAMER_Y, S_HEIGHT-FRAMER_Y), (0, W_HEIGHT)))
                #smoothening
                clocX = plocX + (index_x - plocX) / SMOOTHENING
                clocY = plocY + (index_y - plocY) / SMOOTHENING
                MOUSE.position = (clocX, clocY)

            if(MOUSE_CLICKABLE and length >= 0.025 and length <= 0.05):
                self.program_log.setText("click!: {:.3f}".format(length))
                MOUSE.click(Button.left, 1)
                MOUSE_CLICKABLE = False

            else:
                self.program_log.setText("not click: {:.3f}".format(length))
            
            plocX, plocY = clocX, clocY
            ht.cur_landmark = (None, None)
            
    
    def convert_cv_qt(self, cv_img):
        #Convert from an opencv image to QPixmap
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(S_WIDTH / 2, S_HEIGHT /2, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    #END FOR VIDEO

    
    def closeHand(self):
        global HANDTRACKED
        self.handTrackingBtn.disconnect()
        self.handTrackingBtn.clicked.connect(self.initVideo)
        self.border_label.setVisible(False)
        self.image_label.setVisible(False)
        if HANDTRACKED:
            HANDTRACKED = False
            self.thread.stop()
    
    
    def closeEvent(self, event):
        global PCIDS
        global HANDTRACKED
        for pcid in PCIDS[:]:
            try:
                sh.kill('-9', pcid)
                PCIDS.remove(pcid)
            except:
                print("ERROR: Cannot Kill PCID: {} in closeEvent!".format(pcid))
 
        try:    
           sh.pkill('-o', 'chromium')
        except:
           print('no chromium')
           
        if self.embeddedApp1:
            self.embeddedApp1.close()
        if self.embeddedApp2:
            self.embeddedApp2.close()
        if HANDTRACKED:
            HANDTRACKED = False
            self.thread.stop()
        os.system('DISPLAY=:0 xrandr -x')
        print("Closing...")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())



"""
    def embed_app1(self, appname, args):
        if not self.embeddedApp1 or not self.embeddedApp1.isEnabled():
            self.embeddedApp1 = embed.EmbeddedApp(appname, args)
            if not self.embeddedApp1:
                self.program_log.setText("App not opened!")
                return
            
            global PCIDS
            PCIDS.append(self.embeddedApp1.pcid)
            
            self.program_log.setText("App opened")
            self.layout().addWidget(self.embeddedApp1, 1, 2, 2, 1)
        
        elif not self.embeddedApp1.isVisible() and self.embeddedApp1.isEnabled():
            self.program_log.setText("maximized embedApp")
            self.embeddedApp1.setVisible(True)
        else:
            self.program_log.setText('passed')
        if HANDTRACKED:
            self.closeHand()
            self.initVideo()
"""  