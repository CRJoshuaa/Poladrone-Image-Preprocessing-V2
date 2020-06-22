from PyQt5.QtWidgets import QApplication,QDialog,QTabWidget,QWidget,QFileDialog,QMessageBox,QErrorMessage
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import cv2

from rename_controller import Rename_Controller

class Rename_View(QWidget):
    def __init__(self,main_controller):
        super().__init__()

        self.main_controller=main_controller
        self.rename_controller=Rename_Controller(self,main_controller)

        style_button="background-color: #FD3A41; \
                        color: #FFFFFF;\
                        border:6px solid #FC0A32;\
                        border-radius:15px;\
                        display:inline-block;\
                        font-family:Arial;\
	                    font-size:14px;\
	                    font-weight:bold;\
                        "
        style_text_field="padding: 0px;\
                            font-size: 12px;\
                            border-width: 2px;\
                            border-color: #FD3A41;\
                            background-color: #FFFFFF;\
                            color: #000000;\
                            border-style: dashed;\
                            border-radius: 12px;\
                            "

        self.renameImagePath=""

        self.label_rename_folder = QtWidgets.QLabel(self)
        self.label_rename_folder.setGeometry(QtCore.QRect(70, 80, 351, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_rename_folder.setFont(font)
        self.label_image_set_name = QtWidgets.QLabel(self)
        self.label_image_set_name.setGeometry(QtCore.QRect(70, 140, 121, 21))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.label_image_set_name.setFont(font)
        self.button_rename_explorer = QtWidgets.QPushButton(self)
        self.button_rename_explorer.setGeometry(QtCore.QRect(600, 80, 81, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.button_rename_explorer.setFont(font)
        self.entry_image_set_name = QtWidgets.QLineEdit(self)
        self.entry_image_set_name.setGeometry(QtCore.QRect(240, 140, 311, 21))
        self.button_rename_execute = QtWidgets.QPushButton(self)
        self.button_rename_execute.setGeometry(QtCore.QRect(370, 350, 81, 31))

        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.button_rename_execute.setFont(font)

        #retranslate part
        self.label_rename_folder.setText("Selected Image Directory")
        self.label_image_set_name.setText("Image Set Name:")

        self.button_rename_explorer.setText("Browse")
        self.button_rename_explorer.setStyleSheet(style_button)
        self.button_rename_explorer.clicked.connect(lambda:self.rename_controller.browseFiles())

        self.entry_image_set_name.setStyleSheet(style_text_field)
        self.button_rename_execute.setText("Rename")
        self.button_rename_execute.setStyleSheet(style_button)
        self.button_rename_execute.clicked.connect(lambda:self.rename_controller.renameFunction())


    def errorMessageBox(self,title,text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()
