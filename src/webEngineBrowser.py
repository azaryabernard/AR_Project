import customStyleSheet as cs
from urllib.parse import urlparse
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget
 
class Browser(QWidget):
    def __init__(self, size=[800,800], default_url='https://www.google.com'):
        #init and frame setup
        super().__init__()
        self.frame = QFrame(self)
        self.frame.resize(size[0],size[1])
        self.frame.setStyleSheet(cs.webBrowser_style)
        self.resize(size[0],size[1])

        #Setup WebEngine WebView
        self.web = QWebEngineView()
        self.web.load(QUrl(default_url))

        #TOOLBAR
        self.horizontalLayout = QHBoxLayout()
        self.url_line = QLineEdit(self.frame)
        self.back_button = QPushButton('<<', self.frame)
        self.forward_button = QPushButton('>>', self.frame)
        self.min_button = QPushButton('—', self.frame)
        self.close_button = QPushButton('X', self.frame)
        [x.setStyleSheet(cs.small_icon_style) for x in [self.back_button, self.forward_button, self.min_button, self.close_button]]
        self.url_line.setStyleSheet(cs.small_line_style)
        
        #Connect toolbar items
        self.back_button.clicked.connect(self.web.back)
        self.forward_button.clicked.connect(self.web.forward)
        self.min_button.clicked.connect(lambda x: self.setVisible(x), False)
        self.close_button.clicked.connect(self.webclose)
        self.url_line.returnPressed.connect(self.browse)
        self.url_line.setText(default_url)
        self.web.urlChanged.connect(lambda url: self.url_line.setText(url.toString()))

        #Add toolbars item to hlayout
        self.horizontalLayout.addWidget(self.back_button, 1)
        self.horizontalLayout.addWidget(self.forward_button, 1)
        self.horizontalLayout.addWidget(self.url_line, 8)
        self.horizontalLayout.addWidget(self.min_button, 1)
        self.horizontalLayout.addWidget(self.close_button, 1)

        #QUICK ACCESS TOOLBAR
        self.quickAccessLayout = QHBoxLayout()
        self.quickAccessLayout.setContentsMargins(1,1,1,1)
        self.quickAccessLayout.setSpacing(5)
        self.fav_buttons = [QPushButton(s, self) for s in ["Google", "YouTube", "GMail", "Twitter", "Instagram", "reddit"]]
        [btn.clicked.connect(lambda state, x="www."+ btn.text() +".com": self.browse(fav=x)) for btn in self.fav_buttons]
        [self.quickAccessLayout.addWidget(btn) for btn in self.fav_buttons]
        [btn.setStyleSheet(cs.small_icon_style) for btn in self.fav_buttons]

        #Add everything to one layout
        self.vertLayout = QVBoxLayout(self.frame)
        self.vertLayout.setContentsMargins(1,1,1,1)
        self.vertLayout.setSpacing(1)
        self.vertLayout.addLayout(self.horizontalLayout)
        self.vertLayout.addWidget(self.web)
        self.vertLayout.addLayout(self.quickAccessLayout)

    #browse the given url both from url_line in toolbar and from QuickAccess Toolbar
    def browse(self, fav=''):
        if fav:
            self.url_line.setText(fav)
        if self.url_line.text():
            parsedUrl = ''
            domain = urlparse(self.url_line.text()).netloc
            if domain:
                parsedUrl = "https://" + domain
            else:
                siteOnly = self.url_line.text().split("www.")
                if len(siteOnly) == 1:
                    parsedUrl = "https://www." + siteOnly[0]
                else:
                    parsedUrl = "https://www." + siteOnly[1]
            if parsedUrl:
                self.web.load(QUrl(parsedUrl))

    #close and set enabled to false (for if in main)
    def webclose(self):
        self.web.close()
        self.setEnabled(False)
        self.close()
