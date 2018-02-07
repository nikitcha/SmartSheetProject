import subprocess
import os
import traceback
import sys
import glob
from PyQt4 import QtGui, QtCore

# Absolute path to Ghostscript executable or command name if Ghostscript is in PATH.
GHOSTSCRIPTCMD = "gswin64"

def pdf_to_png(pdffilepath, resolution, pngpath=''):
    if not os.path.isfile(pdffilepath):
        print("'%s' is not a file. Skip." % pdffilepath)

    pdffiledir = os.path.dirname(pdffilepath)
    if not pngpath:
        pngpath = pdffiledir
    
    pdffilename = os.path.basename(pdffilepath)
    pdfname, ext = os.path.splitext(pdffilename)

    try:    
        # Change the "-rXXX" option to set the PNG's resolution.
        # http://ghostscript.com/doc/current/Devices.htm#File_formats
        # For other commandline options see
        # http://ghostscript.com/doc/current/Use.htm#Options
        arglist = [GHOSTSCRIPTCMD,
                  "-q",                     
                  "-dQUIET",                   
                  "-dPARANOIDSAFER",                    
                  "-dBATCH",
                  "-dNOPAUSE",
                  "-dNOPROMPT",                  
                  "-sOutputFile=" + os.path.join(pngpath, pdfname) + "-%03d.png",
                  "-sDEVICE=png16m",                  
                  "-r%s" % resolution,
                  pdffilepath]
        print("Running command:\n%s" % ' '.join(arglist))
        sp = subprocess.Popen(
            args=arglist,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    except OSError:
        sys.exit("Error executing Ghostscript ('%s'). Is it in your PATH?" %
            GHOSTSCRIPTCMD)            
    except:
        print("Error while running Ghostscript subprocess. Traceback:")
        print("Traceback:\n%s"%traceback.format_exc())

    stdout, stderr = sp.communicate()
    print("Ghostscript stdout:\n'%s'" % stdout)
    if stderr:
        print("Ghostscript stderr:\n'%s'" % stderr)
    
    return glob.glob(os.path.join(pngpath, pdfname) + '*.png')
      
class RectItem(QtGui.QGraphicsRectItem):
    def __init__(self, parent=None):
        QtGui.QGraphicsPixmapItem.__init__(self, parent)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)

        # set item's rectangle
        self.setRect(QtCore.QRectF(50, 50, 100, 100))
        self.setBrush(QtGui.QColor(250,100,200,100))
        self.setPen(QtCore.Qt.darkCyan)

    def mouseMoveEvent(self, event):
        # check of mouse moved within the restricted area for the item 
        #if self.move_restrict_rect.contains(event.scenePos()):
        QtGui.QGraphicsRectItem.mouseMoveEvent(self, event)

class SheetGui(QtGui.QWidget):
    def __init__(self, audio , omr, png, parent=None):
        super(SheetGui, self).__init__(parent)
        self.audio = audio
        self.omr = omr
        self.png = png 
        
        self.scene = QtGui.QGraphicsScene(0, 0, 800, 800)

        pic = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(png))
        pic.setOffset(0,30)
        self.scene.addItem(pic)
        
        rectItem = RectItem()
        self.scene.addItem(rectItem)

        self.view = QtGui.QGraphicsView()
        self.view.setScene(self.scene)
        self.view.setGeometry(QtCore.QRect(0, 0, 800, 800))
        
        self.bplay = QtGui.QPushButton("Play")
        self.bstop = QtGui.QPushButton("Stop")        
        self.bplay.clicked.connect(self.play)
        self.bstop.clicked.connect(self.stop)
        
        layout = QtGui.QVBoxLayout()        
        layout.addWidget(self.bplay)
        layout.addWidget(self.bstop)
        layout.addWidget(self.view)
        self.setLayout(layout)
        
    def play(self):
        wav = self.audio.wav()
        self.audio.play(wav)
    
    def stop(self):
        self.audio.stop()