from PyQt5.QtWidgets import QApplication,QDialog,QTabWidget,QWidget,QFileDialog,QMessageBox,QErrorMessage
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import cv2


class Rename_Controller():
    def __init__(self,view,main_controller):
        self.view=view
        self.main_controller=main_controller

    def browseFiles(self):
        self.view.renameImagePath=QFileDialog.getExistingDirectory(None,'Browse selected images')


        try:
            if not any(fname.endswith('.JPG') for fname in os.listdir(self.view.renameImagePath)):
                raise Exception("Directory has no .jpeg files")

        except Exception:
            self.view.errorMessageBox("Select a Directory","JPG files(s) not found")
            return


        self.view.label_rename_folder.setText("Selected Directory: "+self.view.renameImagePath)
        self.view.label_rename_folder.adjustSize()

        if (self.view.renameImagePath==""):
            self.view.label_rename_folder.setText("RenameWindow","No Folder Selected")

        self.main_controller.statusBar().showMessage('Standby')
        self.main_controller.progressBar.setValue(0)

    def renameFunction(self):
        try:
            print(self.view.renameImagePath)
            if (self.view.renameImagePath==""):
                raise Exception("Empty Image Directory")

        except AttributeError:
            print("Empty Image Directory")
            self.view.errorMessageBox("Select A Directory","Empty Image Directory")
            return;
        except Exception:
            print("Empty Image Directory")
            self.view.errorMessageBox("Select A Directory","Empty Image Directory")
            return;

        self.step=0
        self.main_controller.progressBar.setValue(self.step)
        self.main_controller.progressBar.setMaximum(len(os.listdir(self.view.renameImagePath)))
        self.main_controller.statusBar().showMessage('Processing')


        if (self.view.entry_image_set_name.text()==""):
            self.imageSetName="default"
        else:
            self.imageSetName=self.view.entry_image_set_name.text().replace(' ',"_")



        for count,filename in enumerate(os.listdir(self.view.renameImagePath)):
            if not(filename.endswith('.JPG')):
                self.step+=1
                self.main_controller.progressBar(self.step)

                continue
            dst=self.imageSetName+str("_"+'{:0>4}'.format(count))+".JPG"
            src=self.view.renameImagePath+'/'+filename
            dst=self.view.renameImagePath+'/'+dst

            os.rename(src,dst)

            self.step+=1
            self.main_controller.progressBar.setValue(self.step)

        self.main_controller.statusBar().showMessage('Complete')
