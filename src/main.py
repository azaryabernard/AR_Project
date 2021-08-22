import sys
import sh
import numpy as np
import handtracking as ht
import customStyleSheet as cs
import webEngineBrowser as wb
import embedded_app as embed
from math import hypot
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt, QSize, pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap, QWindow, QImage
from pynput.mouse import Button, Controller
from _config import *



######################
MOUSE = Controller()
APP_POS = [2,1,3]
PCIDS = []
plocX,plocY = 0, 0
clocX, clocY = 0, 0
######################
        
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AR Prototype 0.1')
        self.resize(W_WIDTH, W_HEIGHT)
        self.setStyleSheet(cs.mainwindow_style);
        self.initUI()
        
        
    def initUI(self):
        lay = QGridLayout()
        lay.setColumnStretch(0, 1)
        lay.setColumnStretch(1, 5)
        lay.setColumnStretch(2, 5)
        lay.setColumnStretch(3, 5)
        lay.setRowStretch(0, 1)
        lay.setRowStretch(1, 2)
        lay.setRowStretch(2, 2)
        lay.setRowStretch(3, 1)
        self.setLayout(lay)
        
        self.init_buttons()
        self.init_labels()
        self.webBrowser = None
        self.embeddedApp = None

        #Timer for updating all widgets
        timer = QTimer(self)
        timer.timeout.connect(self.updateAll)
        timer.start(1000)
    

    def init_buttons(self):
        vertLayout = QVBoxLayout()
        #EXIT BUTTON
        self.exit_button = QPushButton('X', self)
        self.exit_button.resize(37,37)
        self.exit_button.setStyleSheet(cs.exit_button_style)
        self.exit_button.move(W_WIDTH-45, W_HEIGHT-45)
        self.exit_button.clicked.connect(self.close)
        
        #SIDEBAR BUTTONS
        self.browserBtn = QPushButton(self)
        self.browserBtn.setIcon(QIcon('../image/webBrowserIcon.png'))
        self.browserBtn.setStyleSheet(cs.icon_style)
        self.browserBtn.clicked.connect(self.browserBtnClicked)

        self.youtubeBtn = QPushButton(self)
        self.youtubeBtn.setIcon(QIcon('../image/youtubeIcon.png'))
        self.youtubeBtn.setStyleSheet(cs.icon_style)
        self.youtubeBtn.clicked.connect(lambda state, appname='YouTube', args=["--profile-directory=Profile 1", "--app-id=agimnkijcaahngcdmfeangaknmldooml"]: self.embed_app(appname, args))
        
        self.terminalBtn = QPushButton(self)
        self.terminalBtn.setIcon(QIcon('../image/terminalIcon.png'))
        self.terminalBtn.setStyleSheet(cs.icon_style)
        self.terminalBtn.clicked.connect(lambda state, appname='lxterminal', args=["--working-directory=/home/pi/Desktop"]: self.embed_app(appname, args))
        
        self.handTrackingBtn = QPushButton('HT', self)
        self.handTrackingBtn.setStyleSheet(cs.icon_style)
        self.handTrackingBtn.clicked.connect(self.initVideo)
        
        vertLayout.addWidget(self.browserBtn)
        vertLayout.addWidget(self.youtubeBtn)
        vertLayout.addWidget(self.terminalBtn)
        vertLayout.addWidget(self.handTrackingBtn)
        vertLayout.setSpacing(10)
        vertLayout.addStretch()
        self.layout().addLayout(vertLayout, 1, 0, 2, 1)


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
        self.program_log.setStyleSheet(cs.log_style)

        frameX = S_WIDTH / 2
        frameY = S_HEIGHT / 2
        self.image_label = QLabel(self)
        self.image_label.resize(frameX, frameY)
        self.image_label.move((W_WIDTH-frameX)/2, (W_HEIGHT-frameY)/2)
        self.border_label = QLabel(self)
        self.border_label.resize(frameX - FRAMER_X, frameY - FRAMER_Y)
        self.border_label.move((W_WIDTH-frameX)/2 + FRAMER_X/2, (W_HEIGHT-frameY)/2 + FRAMER_Y/2)
        self.border_label.setStyleSheet(cs.ht_border_style) 
        self.border_label.setVisible(False)
        self.image_label.setVisible(False)


    def embed_app(self, appname, args):
        if not self.embeddedApp or not self.embeddedApp.isEnabled():
            self.embeddedApp = embed.EmbeddedApp(appname, args)
            if not self.embeddedApp:
                self.program_log.setText("App not opened!")
                return
            
            global PCIDS
            PCIDS.append(self.embeddedApp.pcid)
            
            self.program_log.setText("App opened")
            if appname == "YouTube":
                self.layout().addWidget(self.embeddedApp, 1, 1, 2, 1)
            elif appname == "lxterminal":
                self.layout().addWidget(self.embeddedApp, 2, 2, 1, 1)
            
            if not self.webBrowser or not self.webBrowser.isEnabled():
                pass
            else:
                size = self.webBrowser.pageSize
                for wp in self.webBrowser.webPages:
                    wp.frame.resize(size[0]-2,size[1])
        
        elif not self.embeddedApp.isVisible() and self.embeddedApp.isEnabled():
            self.program_log.setText("maximized embedApp")
            self.embeddedApp.setVisible(True)
            pass
        else:
            self.program_log.setText('passed')
            pass
        
        
        
    def browserBtnClicked(self):
        browserSize = [588, 672]
        if not self.embeddedApp or not self.embeddedApp.isEnabled():
            pass
        else:
            browserSize = [586, 672]
            
        if not self.webBrowser or not self.webBrowser.isEnabled():
            self.program_log.setText('open browser')
            self.webBrowser = wb.Browser(size=browserSize)
            self.webBrowser.setEnabled(True)
            self.layout().addWidget(self.webBrowser, 1, 3, 2, 1)
            
        elif not self.webBrowser.isVisible() and self.webBrowser.isEnabled():
            self.program_log.setText("maximized browser")
            self.webBrowser.setVisible(True)

        else:
            self.program_log.setText('passed')
            pass
        
    
            

    def updateAll(self):
        global MOUSE_CLICKABLE
        MOUSE_CLICKABLE = True
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.time_label.setText(label_time)
    
    
    #FOR VIDEO
    def initVideo(self):
        global HANDTRACKED
        self.border_label.setVisible(True)
        self.image_label.setVisible(True)

        if(HANDTRACKED):
            self.handTrackingBtn.disconnect()
            self.handTrackingBtn.clicked.connect(self.closeEvent)
            return

        HANDTRACKED = True
        # create the video capture thread,  connect its signal to the update_image, start
        self.thread = ht.VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
    
    
    def closeEvent(self, event):
        global HANDTRACKED
        global PCIDS
        print("Closing...")
        self.handTrackingBtn.disconnect()
        self.handTrackingBtn.clicked.connect(self.initVideo)
        self.border_label.setVisible(False)
        self.image_label.setVisible(False)
        
        if self.embeddedApp:
            for pcid in PCIDS:
                try:
                    sh.kill('-9', pcid)
                except:
                    pass
            self.embeddedApp.close()
            
        if HANDTRACKED:
            HANDTRACKED = False
            self.thread.stop()
        
        
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        global plocX
        global plocY
        global clocX
        global clocY
        global MOUSE_CLICKABLE

        #Updates the image_label with a new opencv image
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        #print(cur_landmark)
        if ht.cur_landmark != (None, None): 
            #convert coordinates
            (index_x, index_y) = (np.interp(ht.cur_landmark[0].x * S_WIDTH, (FRAMER_X, S_WIDTH-FRAMER_X), (0, W_WIDTH)), 
                                    np.interp(ht.cur_landmark[0].y * S_HEIGHT, (FRAMER_Y, S_HEIGHT-FRAMER_Y), (0, W_HEIGHT)))

            length = hypot(ht.cur_landmark[1].x - ht.cur_landmark[0].x, ht.cur_landmark[1].y - ht.cur_landmark[0].y)

            #smoothening
            clocX = plocX + (index_x - plocX) / SMOOTHENING
            clocY = plocY + (index_y - plocY) / SMOOTHENING
            
            #mouse events
            if(length >= 0.1):
                MOUSE.position = (clocX, clocY)

            if(MOUSE_CLICKABLE and length >= 0.022 and length <= 0.06):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.showFullScreen()
    sys.exit(app.exec_())
