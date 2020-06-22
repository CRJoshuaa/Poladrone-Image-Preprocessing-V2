from PyQt5.QtWidgets import QApplication,QDialog,QTabWidget,QWidget,QFileDialog,QMessageBox,QErrorMessage,QProgressBar
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import cv2


class Crop_Controller():
    def __init__(self,view,main_controller):
        super().__init__()
        self.view=view
        self.main_controller=main_controller
        self.displayIndex=0


    def browseFiles(self,label):
        directory=QFileDialog.getExistingDirectory(None,'Select a directory')
        if label==self.view.label_raw_folder:
            #try block for RAW folder with no jpeg
            try:
                if not any(fname.endswith('.JPG') for fname in os.listdir(directory)):
                    label.setText("No Folder Selected ")
                    raise Exception("Directory has no .JPG files")

            except Exception:
                self.view.errorMessageBox("Select A Directory","JPG files(s) not found")
                return

            label.setText("RAW Folder: "+ directory)
            self.view.path=directory
            self.displayImage()

            print(self.view.path)

        else:
            label.setText("Cropped Folder: "+ directory)
            self.view.outPath=directory
            print(self.view.outPath)

        self.main_controller.statusBar().showMessage('Standby')
        self.main_controller.progressBar.setValue(0)

        if (directory==""):
            label.setText("No Folder Selected ")

    def getImagePath(self):
        display_list=os.listdir(self.view.path)
        display_path=os.path.join(self.view.path,display_list[self.displayIndex])
        return display_path

    def setImageIndex(self):
        indexDisplay="Image "+ str(self.displayIndex+1)+" of " + str(len(os.listdir(self.view.path)))
        self.view.label_image_index.setText(indexDisplay)

    def displayImage(self):
        try:
            if self.view.path=="":
                raise Exception("RAW folder has not been selected")

        except Exception:
            self.view.errorMessageBox("Crop Sections","RAW Folder has not been selected")
            return

        if(self.view.check_dimension_lock.isChecked()):
            self.recLength=self.view.entry_crop_length.value()
            self.recWidth=self.view.entry_crop_length.value()
        else:
            self.recLength=self.view.entry_crop_length.value()
            self.recWidth=self.view.entry_crop_width.value()

        # convert image file into pixmap
        pixmap_image = QtGui.QPixmap(self.getImagePath())

        # create painter instance with pixmap
        painterInstance = QtGui.QPainter(pixmap_image)
        #painterInstance.begin()

        # set rectangle color and thickness
        penRectangle = QtGui.QPen(QtCore.Qt.red)
        penRectangle.setWidth(20)

        # draw rectangle on painter
        painterInstance.setPen(penRectangle)

        # for loading color image
        img_to_crop = cv2.imread(self.getImagePath())
        height, width, channels = img_to_crop.shape

        # new position for square image cropping to size
        upper_left = (int((width / 2) - self.recWidth/2), int((height / 2) - self.recLength/2))
        bottom_right = (int((width / 2) + self.recWidth), int((height / 2) + self.recLength))

        # place rectangle
        painterInstance.drawRect(upper_left[0],upper_left[1],self.recWidth,self.recLength)

        self.view.label_image_display.setPixmap(pixmap_image)
        painterInstance.end()
        self.setImageIndex()

    def checkShape(self):
        if self.view.check_dimension_lock.isChecked():
            self.view.entry_crop_width.setDisabled(True)
            self.view.label_crop_width.setStyleSheet("color:grey")
        else:
            self.view.entry_crop_width.setDisabled(False)
            self.view.label_crop_width.setStyleSheet("color:black")



    def imageNext(self):
        try:
            if self.view.path=="":
                raise Exception("RAW folder has not been selected")

        except Exception:
            self.view.errorMessageBox("Crop Sections","RAW Folder has not been selected")
            return

        if (self.displayIndex<(len(os.listdir(self.view.path))-1)):
            self.displayIndex+=1
            self.displayImage()

    def imagePrevious(self):
        try:
            if self.view.path=="":
                raise Exception("RAW folder has not been selected")

        except Exception:
            self.view.errorMessageBox("Crop Sections","RAW Folder has not been selected")
            return

        if (self.displayIndex>0):
            self.displayIndex-=1
            self.displayImage()





    def cropFunction(self):
        #try block for RAW path
        try:
            print(self.view.path)
            if (self.view.path==""):
                raise Exception("Empty Raw Directory")

        except AttributeError:
            print("Empty RAW Directory")
            self.view.errorMessageBox("Select A Directory","Empty RAW Directory")
            return;

        except Exception:
            print("Empty RAW Directory")
            self.view.errorMessageBox("Select A Directory","Empty RAW Directory")
            return;

        #try block for cropped path
        try:
            if (self.view.outPath==""):
                raise Exception("Empty Cropped Directory")
        except AttributeError:
            self.view.errorMessageBox("Select A Directory","Empty Cropped Directory")
            return;

        except Exception:
            self.view.errorMessageBox("Select A Directory","Empty Cropped Directory")
            return;

        #dimension_lock check
        if(self.view.check_dimension_lock.isChecked()):
            self.cropLength=self.view.entry_crop_length.value()//2
            self.cropWidth=self.view.entry_crop_length.value()//2
        else:
            self.cropLength=self.view.entry_crop_length.value()//2
            self.cropWidth=self.view.entry_crop_width.value()//2

        #initializing progressbar
        self.step=0
        self.main_controller.progressBar.setValue(self.step)
        self.main_controller.progressBar.setMaximum(len(os.listdir(self.view.path)))

        # iterate through the names of contents of the folder
        for image_path in os.listdir(self.view.path):

            # create the full input path and read the file
            input_path = os.path.join(self.view.path, image_path)

            # for loading color image
            img_to_crop = cv2.imread(input_path)
            height, width, channels = img_to_crop.shape


            # new position for square image cropping to size
            upper_left = (int((width / 2) - self.cropWidth), int((height / 2) - self.cropLength))
            bottom_right = (int((width / 2) + self.cropWidth), int((height / 2) + self.cropLength))


            # crop the image
            img_crop = img_to_crop[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]]

            # create full output path & save the file to disk
            fullpath = os.path.join(self.view.outPath, 'crop_'+image_path)
            cv2.imwrite(fullpath, img_crop)

            #update self.main_controller.progressBar
            self.step+=1
            self.main_controller.progressBar.setValue(self.step)

        self.main_controller.statusBar().showMessage('Complete')
