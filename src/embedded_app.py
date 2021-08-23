from time import sleep, time
import sh
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import customStyleSheet as cs

APPLICATIONS_DICT = {
    "lxterminal": "lxterminal",
    "New Tab - Chromium" : "/usr/lib/chromium-browser/chromium-browser",
    "YouTube" : "/usr/bin/chromium",
    "Mozilla Firefox" : "/usr/lib/firefox-esr/firefox-esr"
}

CUR_PCID = None

class Container(QWindow):
    def __init__(self):
        super().__init__()

    def embed(self, appname, args):
        global CUR_PCID
        try:
            command = APPLICATIONS_DICT[appname]
        except:
            return False

        self.proc = QProcess()
        self.proc.setProgram(command)
        self.proc.setArguments(args)
        started, pcid = self.proc.startDetached()
        CUR_PCID = pcid
    
        print(appname)
        print(args)
        print(pcid)
        if(not started):
            return None

        #sleep(3)
        if(appname=='lxterminal'):
            appname = 'pi@raspberrypi: ~/Desktop'
        
        timeout = time() + 10
        while True:
            if time() > timeout:
                print("ERROR EMBED APP")
                return False
            try:    
                winid = int([l for l in sh.xwininfo('-root', '-tree').split('\n') if appname in l][0].split('"' + appname)[0].strip(), 16)
            except:
                continue
            else:
                break
            
        print(hex(winid))
        testWindow = QWindow.fromWinId(winid)
        #testWindow.setFlags(Qt.FramelessWindowHint) CREATE ERROR FOR SOME REASON BADACCESS
        testWindow = QWidget.createWindowContainer(testWindow)
        #testWindow.setWindowFlags(Qt.WindowStaysOnTopHint)
        return testWindow, pcid


class EmbeddedApp(QWidget):
    def __init__(self, appname, args):
        super().__init__()

        try:
            self.appWindow, self.pcid = Container().embed(appname, args)
        except:
            print("error opening app")
            return None
        
        self.min_button = QPushButton('—', self)
        self.close_button = QPushButton(' x ', self)
        self.min_button.clicked.connect(lambda x: self.setVisible(x), False)
        self.close_button.clicked.connect(self.appclose)
        [x.setStyleSheet(cs.no_border_icon_style) for x in [self.min_button, self.close_button]]
        horLayout = QHBoxLayout()
        horLayout.addStretch()
        horLayout.addWidget(self.min_button)
        horLayout.addWidget(self.close_button)
        vertLayout = QVBoxLayout()
        vertLayout.addLayout(horLayout)
        vertLayout.addWidget(self.appWindow)
        vertLayout.setSpacing(0)
        self.setLayout(vertLayout)
        
        
    def appclose(self):
        try:
            sh.kill('-9', self.pcid)
        except:
            print("unable to kill from close button {}".format(self.pcid))
        self.setEnabled(False)
        self.close()
