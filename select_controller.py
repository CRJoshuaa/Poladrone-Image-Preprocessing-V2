from PyQt5.QtWidgets import QApplication,QDialog,QTabWidget,QWidget,QFileDialog,QMessageBox,QErrorMessage
from PyQt5 import QtCore, QtGui, QtWidgets

import os
import shutil
import sys
import cv2

class Select_Controller():
    def __init__(self,view,main_controller):
        self.view=view
        self.main_controller=main_controller

    def browseFiles(self,label):
        directory=QFileDialog.getExistingDirectory(None,'Select a directory')
        if label==self.view.label_cropped_folder:
            #try block for cropped directory
            try:
                if not any(fname.endswith('.JPG') for fname in os.listdir(directory)):
                    label.setText("No Folder Selected ")
                    raise Exception("Directory has no .jpeg files")

            except Exception:
                self.view.errorMessageBox("Select A Directory","JPG files(s) not found")
                return

            label.setText("Cropped Folder: "+ directory)
            self.view.croppedPath=directory
        else:
            label.setText("Selected Folder: "+ directory)
            self.view.selectedPath=directory

        self.main_controller.statusBar().showMessage('Standby')
        self.main_controller.progressBar.setValue(0)

        if (directory==""):
            label.setText("No Folder Selected ")
            raise Exception("Empty directory")



    def selectFunction(self):
        #try block for cropped image path
        try:
            print(self.view.croppedPath)
            if (self.view.croppedPath==""):
                raise Exception("Empty Cropped Directory")

        except AttributeError:
            print("Empty Cropped Directory")
            self.view.errorMessageBox("Select A Directory","Empty Cropped Directory")
            return
        except Exception:
            print("Empty Cropped Directory")
            self.view.errorMessageBox("Select A Directory","Empty Cropped Directory")
            return

        #try block for selected image path
        try:
            print(self.view.selectedPath)
            if (self.view.selectedPath==""):
                raise Exception("Empty Cropped Directory")

        except AttributeError:
            print("Empty Selected Directory")
            self.view.errorMessageBox("Select A Directory","Empty Selected Directory")
            return
        except Exception:
            print("Empty Selected Directory")
            self.view.errorMessageBox("Select A Directory","Empty Selected Directory")
            return

        self.main_controller.statusBar().showMessage('Processing')

        nthNum=int(self.view.entry_nth_number.value())
        list=os.listdir(self.view.croppedPath)

        self.step=0
        self.main_controller.progressBar.setValue(self.step)
        self.main_controller.progressBar.setMaximum(len(list)//nthNum)

        for i in list[::nthNum]:
            if not(i.endswith('.JPG')):
                self.step+=1
                self.main_controller.progressBar.setValue(self.step)
                continue
            shutil.copy(self.view.croppedPath+'/'+i,self.view.selectedPath)
            self.step+=1
            self.main_controller.progressBar.setValue(self.step)

        self.main_controller.statusBar().showMessage('Complete')
