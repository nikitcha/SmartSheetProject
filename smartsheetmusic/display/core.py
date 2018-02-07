from . import helpers
import sys
from PyQt4 import QtGui, QtCore

from PIL import Image, ImageTk

def qt_gui(audio, omr, png):
    app = QtGui.QApplication(sys.argv)
    form = helpers.SheetGui(audio,omr,png)
    form.show()
    app.exec_()
    