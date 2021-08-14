import sys
from time import sleep
import sh
import customStyleSheet as cs
import webEngineBrowser as wb
import embed_terminal_1 as et
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QGridLayout
from PyQt5.QtCore import QTimer, QTime, Qt, QSize
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QWindow

W_WIDTH = 2560
W_HEIGHT = 1440

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AR Prototype 0.1')
        self.resize(W_WIDTH,W_HEIGHT)
        self.setStyleSheet(cs.mainwindow_style);
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
        self.exit_button.resize(50,50)
        self.exit_button.setStyleSheet(cs.exit_button_style)
        self.exit_button.move(W_WIDTH-60, W_HEIGHT-60)
        self.exit_button.clicked.connect(self.close)
        
        #SIDEBAR BUTTONS
        offsetX = 10
        offsetY = 300
        self.browserBtn = QPushButton(self)
        self.browserBtn.setIcon(QIcon('../image/webBrowserIconGray.png'))
        self.browserBtn.setIconSize(QSize(96, 96))
        self.browserBtn.setStyleSheet(cs.icon_style)
        self.browserBtn.resize(125,125)
        self.browserBtn.move(offsetX, offsetY)
        self.browserBtn.clicked.connect(self.browserBtnClicked)


    def init_labels(self):
        self.time_label = QLabel('', self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.resize(200, 80)
        self.time_label.move(W_WIDTH-210, 10)
        self.time_label.setStyleSheet(cs.time_label_style)

        self.program_log = QLabel('Log: ', self)
        self.program_log.setAlignment(Qt.AlignRight)
        self.program_log.resize(200, 40)
        self.program_log.move(10, W_HEIGHT-50)
        self.program_log.setStyleSheet('color:green; font: 20px; border:0px; ')

    
    def browserBtnClicked(self):
        if not self.webBrowser.isEnabled():
            self.program_log.setText('open browser')
            self.webBrowser = wb.Browser()
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