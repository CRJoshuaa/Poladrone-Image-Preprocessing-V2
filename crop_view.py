from PyQt5.QtWidgets import QApplication,QScrollArea,QDialog,QScrollArea,QTabWidget,QWidget,QFileDialog,QMessageBox,QErrorMessage,QProgressBar
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import cv2

from crop_controller import Crop_Controller

class Crop_View(QWidget):
    def __init__(self,main_controller):
        super().__init__()

        self.main_controller=main_controller
        self.crop_controller=Crop_Controller(self,main_controller)

        self.path=""
        self.outPath=""
        style_button="background-color: #FD3A41; \
                        color: #FFFFFF;\
                        border:6px solid #FC0A32;\
                        border-radius:15px;\
                        display:inline-block;\
                        font-family:Arial;\
	                    font-size:14px;\
	                    font-weight:bold;\
                        "
        style_image_browser="background-color:#FD3A41;\
                            	border-radius:15px;\
                            	border:1px solid #FC0A32;\
                            	display:inline-block;\
                            	color:#ffffff;\
                            	font-family:Arial;\
                            	font-size:17px;\
                            	padding:24px 11px;\
                            "

        self.label_raw_folder = QtWidgets.QLabel(self)
        self.label_raw_folder.setGeometry(QtCore.QRect(80, 80, 511, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_raw_folder.setFont(font)
        self.label_raw_folder.setWordWrap(True)

        self.label_crop_folder = QtWidgets.QLabel(self)
        self.label_crop_folder.setGeometry(QtCore.QRect(80, 140, 511, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_crop_folder.setFont(font)
        self.label_crop_folder.setWordWrap(True)
        self.button_raw_explorer = QtWidgets.QPushButton(self)
        self.button_raw_explorer.setGeometry(QtCore.QRect(600, 80, 81, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.button_raw_explorer.setFont(font)
        self.button_crop_explorer = QtWidgets.QPushButton(self)
        self.button_crop_explorer.setGeometry(QtCore.QRect(600, 140, 81, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.button_crop_explorer.setFont(font)
        self.group_dimensions = QtWidgets.QGroupBox(self)
        self.group_dimensions.setGeometry(QtCore.QRect(70, 200, 301, 121))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.group_dimensions.setFont(font)
        self.check_dimension_lock = QtWidgets.QCheckBox(self.group_dimensions)
        self.check_dimension_lock.setGeometry(QtCore.QRect(20, 20, 111, 21))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.check_dimension_lock.setFont(font)
        self.check_dimension_lock.setAutoRepeat(False)
        self.check_dimension_lock.stateChanged.connect(lambda:self.crop_controller.checkShape())
        self.label_crop_length = QtWidgets.QLabel(self.group_dimensions)
        self.label_crop_length.setGeometry(QtCore.QRect(30, 50, 91, 21))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_crop_length.setFont(font)
        self.label_crop_length.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_crop_width = QtWidgets.QLabel(self.group_dimensions)
        self.label_crop_width.setGeometry(QtCore.QRect(30, 80, 91, 21))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_crop_width.setFont(font)
        self.label_crop_width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.entry_crop_length = QtWidgets.QSpinBox(self.group_dimensions)
        self.entry_crop_length.setGeometry(QtCore.QRect(170, 50, 51, 21))

        font = QtGui.QFont()
        font.setPointSize(8)
        self.entry_crop_length.setFont(font)
        self.entry_crop_length.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.entry_crop_length.setMinimum(1)
        self.entry_crop_length.setMaximum(5000)
        self.entry_crop_length.setSingleStep(100)
        self.entry_crop_length.setProperty("value", 500)
        self.entry_crop_width = QtWidgets.QSpinBox(self.group_dimensions)
        self.entry_crop_width.setGeometry(QtCore.QRect(170, 80, 51, 21))

        font = QtGui.QFont()
        font.setPointSize(8)
        self.entry_crop_width.setFont(font)
        self.entry_crop_width.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.entry_crop_width.setMinimum(1)
        self.entry_crop_width.setMaximum(3000)
        self.entry_crop_width.setSingleStep(100)
        self.entry_crop_width.setProperty("value", 500)
        self.button_crop_execute = QtWidgets.QPushButton(self)
        self.button_crop_execute.setGeometry(QtCore.QRect(370, 730, 81, 31))


        #crop sections
        self.group_sections = QtWidgets.QGroupBox(self)
        self.group_sections.setGeometry(QtCore.QRect(70, 330, 581, 391))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.group_sections.setFont(font)
        self.label_image_display = QtWidgets.QLabel(self.group_sections)
        self.label_image_display.setGeometry(QtCore.QRect(50, 30, 471, 261))
        self.label_image_display.setText("")
        self.label_image_display.setScaledContents(True)

        self.button_previous = QtWidgets.QPushButton(self.group_sections)
        self.button_previous.setGeometry(QtCore.QRect(50, 300, 91, 31))

        self.button_refresh = QtWidgets.QPushButton(self.group_sections)
        self.button_refresh.setGeometry(QtCore.QRect(240, 300, 91, 31))

        self.button_next = QtWidgets.QPushButton(self.group_sections)
        self.button_next.setGeometry(QtCore.QRect(430, 300, 91, 31))



        self.label_image_index = QtWidgets.QLabel(self.group_sections)
        self.label_image_index.setGeometry(QtCore.QRect(10, 360, 200, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_image_index.setFont(font)
        #self.label_image_index.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.button_crop_execute.setFont(font)

        self.label_raw_folder.setText("Raw Image Directory")
        self.label_crop_folder.setText("Cropped Image Directory")

        self.button_raw_explorer.setText("Browse")
        self.button_raw_explorer.setStyleSheet(style_button)
        self.button_raw_explorer.clicked.connect(lambda: self.crop_controller.browseFiles(self.label_raw_folder))

        self.button_crop_explorer.setText("Browse")
        self.button_crop_explorer.setStyleSheet(style_button)
        self.button_crop_explorer.clicked.connect(lambda: self.crop_controller.browseFiles(self.label_crop_folder))

        self.group_dimensions.setTitle("Crop Dimensions")
        self.check_dimension_lock.setText("Square Crop")
        self.label_crop_length.setText("Crop Length:")
        self.label_crop_width.setText("Crop Width:")

        self.group_sections.setTitle("Crop Section")

        self.button_previous.setText("Previous")
        self.button_previous.setStyleSheet(style_image_browser)
        self.button_previous.clicked.connect(lambda:self.crop_controller.imagePrevious())

        self.button_refresh.setText("Refresh")
        self.button_refresh.setStyleSheet(style_image_browser)
        self.button_refresh.clicked.connect(lambda:self.crop_controller.displayImage())




        self.button_next.setText("Next")
        self.button_next.setStyleSheet(style_image_browser)
        self.button_next.clicked.connect(lambda:self.crop_controller.imageNext())

        self.button_crop_execute.setText("Crop")
        self.button_crop_execute.setStyleSheet(style_button)
        self.button_crop_execute.clicked.connect(lambda: self.crop_controller.cropFunction())




    def errorMessageBox(self,title,text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()
