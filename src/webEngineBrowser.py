import customStyleSheet as cs
from urllib.parse import urlparse
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget
 

class Browser(QTabWidget):
    """Tab Widget that that can have new tabs easily added to it."""

    def __init__(self, size=[835,895]):
        # Inits and Setup
        super().__init__()
        self.tabNumber = 0
        self.webPages = []
        self.resize(10,10)

        # Corner Widget storing AddTab, minimized browser, close browser
        cornerWidget = QWidget(self)
        toolBar = QHBoxLayout(cornerWidget)
        # Buttons in the corner
        plus_button = QPushButton(' + ', self)
        min_button = QPushButton('—', self)
        close_button = QPushButton(' x ', self)
        # Add widgets
        toolBar.addWidget(plus_button)
        toolBar.addWidget(min_button)
        toolBar.addWidget(close_button)
        self.setCornerWidget(cornerWidget)

        # Stylesheet
        self.setStyleSheet("border-width: 0px;")
        self.tabBar().setStyleSheet("background-color: white;")
        self.cornerWidget().setStyleSheet("background-color: white; border-width: 0px; spacing: 0; border-top-left-radius:10px; border-top-right-radius:10px; margin-right:11px;")
        toolBar.setContentsMargins(10,0,10,0)
        toolBar.setSpacing(0)
        [x.setStyleSheet(cs.no_border_icon_style) for x in [plus_button, min_button, close_button]]

        # Properties
        self.setMovable(True)
        self.setTabsClosable(True)

        # Signals
        self.tabCloseRequested.connect(self.removeTabSelf)
        plus_button.clicked.connect(self.addNewTab)
        min_button.clicked.connect(lambda x: self.setVisible(x), False)
        close_button.clicked.connect(self.webclose)
               
        #DefaultHomePage
        self.addNewTab()
    # end Constructor

    def removeTabSelf(self, index):
        #print("INDEX: {}".format(index))
        self.webPages[index].web.close()
        self.removeTab(index)
        self.webPages.pop(index)
        newInd = 0
        for wp in self.webPages:
            wp.web.urlChanged.disconnect()
            wp.web.urlChanged.connect(lambda state, x=newInd: self.url_change(x, state))
            newInd = newInd + 1
        
        self.tabNumber = self.tabNumber - 1
        if self.tabNumber == 0:
            self.webclose()

    def addNewTab(self):
        webPage = WebPage()
        self.webPages.append(webPage)
        self.addTab(webPage, "https://www.google.com/")        
        index = self.tabNumber
        self.setTabText(index, "google")
        webPage.web.urlChanged.connect(lambda state, x=index: self.url_change(x, state))
        self.tabNumber = self.tabNumber + 1

    
    def url_change(self, index, url):
        splitUrl = url.toString().split('.')
        usedUrl = "Unknown"
        
        if len(splitUrl) == 2:
            usedUrl = splitUrl[0].split('//')[1]
        elif len(splitUrl) == 3:
            usedUrl = splitUrl[1]
            
        self.setTabText(index, usedUrl)
        self.webPages[index].url_line.setText(url.toString())

    
    def webclose(self):
        for tb_ind in range(self.tabNumber):
            self.webPages[tb_ind].web.close()
            self.webPages[tb_ind].close()
            
        self.setEnabled(False)
        self.close()
# end class CustomTabWidget


class WebPage(QWidget):
    def __init__(self, size=[835,895], default_url='https://www.google.com'):
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
        [x.setStyleSheet(cs.small_icon_style) for x in [self.back_button, self.forward_button]]
        self.url_line.setStyleSheet(cs.small_line_style)
        
        #Connect toolbar items
        self.back_button.clicked.connect(self.web.back)
        self.forward_button.clicked.connect(self.web.forward)
        self.url_line.returnPressed.connect(self.browse)
        self.url_line.setText(default_url)

        #Add toolbars item to hlayout
        self.horizontalLayout.addWidget(self.back_button, 1)
        self.horizontalLayout.addWidget(self.forward_button, 1)
        self.horizontalLayout.addWidget(self.url_line, 8)

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
        self.web.setAttribute(Qt.WA_DeleteOnClose)

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
