from PyQt5.QtWidgets import QApplication,QDialog,QTabWidget,QWidget,QFileDialog,QMessageBox,QErrorMessage
from PyQt5 import QtCore, QtGui, QtWidgets

import os
import shutil
import sys
import cv2

from select_controller import Select_Controller


class Select_View(QWidget):
    def __init__(self,main_controller):
        super().__init__()

        self.main_controller=main_controller
        self.select_controller=Select_Controller(self,main_controller)

        style_button="background-color: #FD3A41; \
                        color: #FFFFFF;\
                        border:6px solid #FC0A32;\
                        border-radius:15px;\
                        display:inline-block;\
                        font-family:Arial;\
	                    font-size:14px;\
	                    font-weight:bold;\
                        "

        croppedPath=""
        selectedPath=""

        self.label_cropped_folder = QtWidgets.QLabel(self)
        self.label_cropped_folder.setGeometry(QtCore.QRect(70, 80, 521, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_cropped_folder.setFont(font)
        self.label_cropped_folder.setWordWrap(True)
        self.label_selection_folder = QtWidgets.QLabel(self)
        self.label_selection_folder.setGeometry(QtCore.QRect(70, 140, 521, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_selection_folder.setFont(font)
        self.label_selection_folder.setWordWrap(True)
        self.button_cropped_explorer = QtWidgets.QPushButton(self)
        self.button_cropped_explorer.setGeometry(QtCore.QRect(600, 80, 81, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.button_cropped_explorer.setFont(font)
        self.button_selection_explorer = QtWidgets.QPushButton(self)
        self.button_selection_explorer.setGeometry(QtCore.QRect(600, 140, 81, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.button_selection_explorer.setFont(font)
        self.label_nth_number = QtWidgets.QLabel(self)
        self.label_nth_number.setGeometry(QtCore.QRect(70, 210, 101, 21))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_nth_number.setFont(font)
        self.button_select_execute = QtWidgets.QPushButton(self)
        self.button_select_execute.setGeometry(QtCore.QRect(370, 350, 81, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.button_select_execute.setFont(font)
        self.entry_nth_number = QtWidgets.QSpinBox(self)
        self.entry_nth_number.setGeometry(QtCore.QRect(170, 210, 51, 21))

        font = QtGui.QFont()
        font.setPointSize(8)
        self.entry_nth_number.setFont(font)
        self.entry_nth_number.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.entry_nth_number.setMinimum(2)
        self.entry_nth_number.setMaximum(50)
        self.entry_nth_number.setSingleStep(1)
        self.entry_nth_number.setProperty("value", 2)

        #retranslate
        self.label_cropped_folder.setText("Cropped Image Directory")
        self.label_selection_folder.setText("Selected Image Directory")

        self.button_cropped_explorer.setText("Browse")
        self.button_cropped_explorer.setStyleSheet(style_button)
        self.button_cropped_explorer.clicked.connect(lambda:self.select_controller.browseFiles(self.label_cropped_folder))

        self.button_selection_explorer.setText("Browse")
        self.button_selection_explorer.setStyleSheet(style_button)
        self.button_selection_explorer.clicked.connect(lambda:self.select_controller.browseFiles(self.label_selection_folder))

        self.label_nth_number.setText("Nth Number:")

        self.button_select_execute.setText("Select")
        self.button_select_execute.setStyleSheet(style_button)
        self.button_select_execute.clicked.connect(lambda:self.selectFunction())



    def errorMessageBox(self,title,text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()
