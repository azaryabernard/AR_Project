import sh
import sys
from _config import W_WIDTH, W_HEIGHT
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtGui import QWindow
from time import sleep, time



        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AR VIEWER FOR AUGMA')
        self.resize(2560, 1440)
        self.initUI()
        
        
    def initUI(self):
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 240, 0, 240)
        
        appnames = ["AUGMA (" , "AR Prototype"]
        windows = []
        
        for appname in appnames:
            timeout = time() + 10
            while True:
                sleep(.1)
                if time() > timeout:
                    print("ERROR EMBED APP")
                    return False
                try:    
                    winid = int([l for l in sh.xwininfo('-root', '-tree').split('\n') if appname in l][0].split('"' + appname)[0].strip(), 16)
                except:
                    try:
                        winid = int([l for l in sh.xwininfo('-root', '-tree').split('\n') if appname in l][1].split('"' + appname)[0].strip(), 16)
                    except:
                        print("error looking for winid")
                        continue
                    else:
                        break
                    continue
                else:
                    break
                
            print(hex(winid))
            testWindow = QWindow.fromWinId(winid)
            testWindow = QWidget.createWindowContainer(testWindow)
            #hlayout.addWidget(testWindow)
            windows.append(testWindow)
        
        #windows[0].move(0, 240)
        #windows[0].resize(W_WIDTH, W_HEIGHT)
        #windows[1].move(1280, 240)
        #windows[1].resize(W_WIDTH, W_HEIGHT)
        
        hlayout.addWidget(windows[0])
        sleep(1)
        hlayout.addWidget(windows[1])
        self.setLayout(hlayout)
        #self.setStyleSheet("background-color: black; border-image: none;")
        exitBtn = QPushButton('x', self)
        exitBtn.resize(30, 30)
        exitBtn.move(2520, 10)
        exitBtn.clicked.connect(self.close)
        


if __name__ == '__main__':
	app = QApplication(sys.argv)
	mw = MainWindow()
	mw.showFullScreen()
	sys.exit(app.exec_())