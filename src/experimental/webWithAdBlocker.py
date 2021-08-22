from PyQt5 import QtCore, QtWidgets, QtWebEngineCore, QtWebEngineWidgets
from adblockparser import AdblockRules

with open("../text/easylist.txt") as f:
    raw_rules = f.readlines()
    rules = AdblockRules(raw_rules)

class WebEngineUrlRequestInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if rules.should_block(url):
            print("block::::::::::::::::::::::", url)
            info.block(True)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    interceptor = WebEngineUrlRequestInterceptor()
    QtWebEngineWidgets.QWebEngineProfile.defaultProfile().setRequestInterceptor(interceptor)
    view = QtWebEngineWidgets.QWebEngineView()
    view.load(QtCore.QUrl("https://www.youtube.com/"))
    view.show()
    sys.exit(app.exec_())
