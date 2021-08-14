from PyQt5.QtWidgets import QTabWidget, QPushButton
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QTabWidget, QWidget
#import gi
#from gi.repository import Wnck, Gdk
import time
import sys

class Container(QtGui.QWindow):
    def __init__(self):
        super().__init__()
        self.embed("/usr/lib/firefox-esr/firefox-esr")

    def embed(self, command, *args):
        self.proc = QtCore.QProcess()
        self.proc.setProgram(command)
        self.proc.setArguments(args)
        self.started = self.proc.startDetached()
