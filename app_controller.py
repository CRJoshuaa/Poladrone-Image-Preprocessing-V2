from PyQt5.QtWidgets import QApplication,QMainWindow,QScrollArea,QStatusBar,QDialog,QTabWidget,QVBoxLayout,QProgressBar
from PyQt5 import QtCore, QtGui, QtWidgets

from crop_view import Crop_View
from select_view import Select_View
from rename_view import Rename_View

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Poladrone Image Processing")
        self.setWindowIcon(QtGui.QIcon('poladroneLogo.png'))
        self.resize(820, 460)
        #self.setMaximumSize(QtCore.QSize(820, 460))

        self.statusBar().showMessage('Ready')
        self.progressBar=QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)

        self.progressBar.setGeometry(30, 40, 200, 20)
        self.progressBar.setValue(0)





        #tab management
        self.tabWidget=QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.addTab(Crop_View(self),"Crop")
        self.tabWidget.addTab(Select_View(self),"Select")
        self.tabWidget.addTab(Rename_View(self),"Rename")





app=QApplication(sys.argv)
win=MainWindow()
win.show()

sys.exit(app.exec_())
