# CODE FROM: https://stackoverflow.com/questions/46250829/how-to-embed-selenium-firefox-browser-into-pyqt4-frame 
# EDITED TO PYQT5

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView


import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QFrame, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton

class Browser(QWidget):

    def __init__(self, size=[800,600], frame=None, centralWidget=None, default_url='https://www.google.com', backButton=True, forwardButton=True, topBar=True):
        """
            Initialize the browser GUI and connect the events
        """

        self.showBackButton = backButton
        self.showForwardButton = forwardButton
        self.showTopBar = topBar


        super().__init__()
        self.resize(size[0],size[1])
        if (centralWidget == None):
            self.centralwidget = QWidget(self)
        else:
            self.centralwidget = centralWidget

        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(1,1,1,1)

        if (frame == None):
            self.frame = QFrame(self.centralwidget)
        else:
            self.frame = frame

        self.gridLayout = QVBoxLayout(self.frame)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setSpacing(0)

        self.horizontalLayout = QHBoxLayout()
        if (self.showTopBar):
            self.tb_url = QLineEdit(self.frame)
        if (self.showBackButton):
            self.bt_back = QPushButton(self.frame)
        if (self.showForwardButton):
            self.bt_ahead = QPushButton(self.frame)

        if (self.showBackButton):
            self.bt_back.setIcon(QIcon().fromTheme("go-previous"))
        if (self.showForwardButton):
            self.bt_ahead.setIcon(QIcon().fromTheme("go-next"))

        if (self.showBackButton):
            self.horizontalLayout.addWidget(self.bt_back)
        if (self.showForwardButton):
            self.horizontalLayout.addWidget(self.bt_ahead)
        if (self.showTopBar):
            self.horizontalLayout.addWidget(self.tb_url)
        self.gridLayout.addLayout(self.horizontalLayout)

        self.html = QWebEngineView()
        self.html.settings().globalSettings().setAttribute(self.html.settings().PluginsEnabled, True)
        self.html.settings().globalSettings().setAttribute(self.html.settings().AutoLoadImages, True)
        self.gridLayout.addWidget(self.html)
        self.mainLayout.addWidget(self.frame)
        #self.setCentralWidget(self.centralwidget)  ---  Not needed when embedding into a frame

        if (self.showTopBar):
            self.tb_url.returnPressed.connect(self.browse)
        if (self.showBackButton):
            self.bt_back.clicked.connect(self.html.back)
        if (self.showForwardButton):
            self.bt_ahead.clicked.connect(self.html.forward)
        self.html.urlChanged.connect(self.url_changed)

        self.default_url = default_url
        if (self.showTopBar):
            self.tb_url.setText(self.default_url)
        self.open(self.default_url)

    def browse(self):
        """
            Make a web browse on a specific url and show the page on the
            Webview widget.
        """

        if (self.showTopBar):
            url = self.tb_url.text() if self.tb_url.text() else self.default_url
            self.html.load(QUrl(url))
            self.html.show()
        else:
            pass

    def url_changed(self, url):
        """
            Triggered when the url is changed
        """
        if (self.showTopBar):
            self.tb_url.setText(url.toString())
        else:
            pass

    def open(self, url):
        self.html.load(QUrl(url))
        self.html.show()

app = QApplication(sys.argv)
window = QWidget()

window.resize(800,600)
myFrame = QFrame(window)
myFrame.resize(800,600)
myFrame.move(10,10)

main = Browser(centralWidget=myFrame, default_url='https://youtu.be/teOtRbZdTs8', forwardButton=True, backButton=True, topBar=True)