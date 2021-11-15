#!/usr/bin/env python

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import glob
import time
import subprocess
import os
from pathlib import Path
import sys
import shutil
import csv
import json
from utils import createleftbuttons, createrightbuttons, createleftbottombox, createletflastbox, extractImages

__appname__ = 'ThesisProjectGUI'

class ImageWindow(QWidget):
    def __init__(self, parent=None):
        super(ImageWindow, self).__init__(parent)
        
        self.targetDirPath = ''
        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftGroupBox()
        self.createBottomRightGroupBox()
        self.createLastLeftGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox)
        mainLayout.addWidget(self.topRightGroupBox,0,1)
        mainLayout.addWidget(self.bottomLeftGroupBox)
        mainLayout.addWidget(self.bottomRightGroupBox,1,1)
        mainLayout.addWidget(self.lastLeftGroupBox,1,2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Styles")

    def createTopLeftGroupBox(self):
        createleftbuttons(self)  

    def createTopRightGroupBox(self):
        createrightbuttons(self)  

    def createBottomLeftGroupBox(self):
        createleftbottombox(self,'image')

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox()

        self.originalImage = QLabel(self)
        self.yoloDetectImage = QLabel(self)
        self.originalImage.setText('Original Image')
        self.yoloDetectImage.setText('Yolo Detection')
        self.originalpixmap = QPixmap()
        self.yolopixmap = QPixmap()
        self.originalImage.setPixmap(self.originalpixmap)
        self.yoloDetectImage.setPixmap(self.yolopixmap)
        self.originalImage.setFixedSize(250, 250)
        self.originalImage.setScaledContents(True)
        self.originalImage.setEnabled(True)
        self.yoloDetectImage.setEnabled(True)
        self.yoloDetectImage.setFixedSize(250, 250)
        self.yoloDetectImage.setScaledContents(True)
        self.originalImage.setStyleSheet("border : 2px solid black;")
        self.yoloDetectImage.setStyleSheet("border : 2px solid black;")

        layout = QHBoxLayout()
        layout.addWidget(self.originalImage)
        layout.addWidget(self.yoloDetectImage)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)

    def createLastLeftGroupBox(self):
        createletflastbox(self)


    def openDirDialog(self, _value=False, dirpath=None, silent=False):
        defaultOpenDirPath = dirpath if dirpath else '.'
        if silent!=True :
            self.targetDirPath = str(QFileDialog.getExistingDirectory(self,
                                                         '%s - Open Directory' % __appname__, defaultOpenDirPath,
                                                         QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        
        self.ProcessSelectedImages()

    def ProcessSelectedImages(self):
        
        ImagesList = glob.glob(self.targetDirPath+'/*.jpg')
        if len(ImagesList) > 0:
            self.progress = QProgressDialog('Processing the Data', 'Done', 0, 100, self)
            self.progress.setWindowModality(Qt.WindowModal)
            self.progress.setGeometry(200, 150, 200, 30) 
            self.progress.setCancelButton(None)
            self.progress.show()
            self.progress.setValue(0)
            if os.path.isdir('runs'):
                shutil.rmtree('runs')
            self.progress.setValue(12)
            detecteionOutput = subprocess.check_output(["python3", "detection_framework/detect.py","--weights", "best.pt", "--img", "640", "--conf", "0.2", "--source", self.targetDirPath], universal_newlines=True)
            self.progress.setValue(100)
        else:
            QMessageBox.about(self,"Info",
                                     'Please select the correct source folder with images !!!')
            

    def startProcessImages(self):
        self.imageProcessing = True
        with open('detections.json') as json_file:
            detection_results_data  = json.load(json_file)
        ImagesList = glob.glob(self.targetDirPath+'/*.jpg')
        if len(ImagesList) > 0:
            for imagepath in ImagesList:

                print(detection_results_data[os.path.basename(imagepath)])
                if (self.imageProcessing == True): 
                    OutputImage = os.path.dirname(os.path.realpath(__file__))+'/runs/detect/exp/'+os.path.basename(imagepath)

                    self.detectionspeedline.setText(" {:0.3f}".format(detection_results_data[os.path.basename(imagepath)]['detection_time']))
                    if len(detection_results_data[os.path.basename(imagepath)]['confidence']) > 0:
                        self.probabilityline.setText(" {:0.3f}".format(max(detection_results_data[os.path.basename(imagepath)]['confidence'])))
                    self.fpsrateline.setText(str(detection_results_data['FPS']))
                    QApplication.processEvents()
                    testimage = QPixmap(imagepath)
                    self.originalImage.setPixmap(testimage)
                    yoloOutputImage = QPixmap(OutputImage)
                    self.yoloDetectImage.setPixmap(yoloOutputImage)                    
                    QApplication.processEvents()
                    time.sleep(2)
                else:
                    break
        else:
            QMessageBox.about(self,"Info",
                                     'Please select the source folder first !!!')

    def stopProcessImages(self):
        if (self.imageProcessing == True):
            self.imageProcessing = False
            QApplication.processEvents()

class VideoWindow(QWidget):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftGroupBox()
        self.createBottomRightGroupBox()
        self.createLastLeftGroupBox()
        self.createLastRightGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox)
        mainLayout.addWidget(self.topRightGroupBox,0,1)
        mainLayout.addWidget(self.bottomLeftGroupBox)
        mainLayout.addWidget(self.bottomRightGroupBox,1,1)
        mainLayout.addWidget(self.lastLeftGroupBox,1,2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Styles")

    def createTopLeftGroupBox(self):
        createleftbuttons(self)  

    def createTopRightGroupBox(self):
        createrightbuttons(self)   

    def createBottomLeftGroupBox(self):
        createleftbottombox(self,'video')

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox()

        self.originalVideo = QLabel(self)
        self.yoloDetectImage = QLabel(self)
        self.originalVideo.setText('Original Video')
        self.yoloDetectImage.setText('Yolo Detection')
        self.originalpixmap = QPixmap()
        self.yolopixmap = QPixmap()
        self.originalVideo.setPixmap(self.originalpixmap)
        self.yoloDetectImage.setPixmap(self.yolopixmap)
        self.originalVideo.setFixedSize(250, 250)
        self.originalVideo.setScaledContents(True)
        self.yoloDetectImage.setFixedSize(250, 250)
        self.yoloDetectImage.setScaledContents(True)
        self.originalVideo.setStyleSheet("border : 2px solid black;")
        self.yoloDetectImage.setStyleSheet("border : 2px solid black;")

        layout = QHBoxLayout()
        layout.addWidget(self.originalVideo)
        layout.addWidget(self.yoloDetectImage)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)

    def createLastLeftGroupBox(self):
        createletflastbox(self)

    def createLastRightGroupBox(self):
        self.lastRightGroupBox = QGroupBox()

    def openDirDialog(self, _value=False, dirpath=None, silent=False):
        defaultOpenDirPath = dirpath if dirpath else '.'
        if silent!=True :
            self.targetDirPath = QFileDialog.getOpenFileName(self,
                                                         '%s - Select File' % __appname__, defaultOpenDirPath
                                                        )
            print(self.targetDirPath[0])
        self.ProcessSelectedImages()
    
    def ProcessSelectedImages(self):
        if len(self.targetDirPath[0]) > 0:
            [f.unlink() for f in Path("tmp_video_images").glob("*") if f.is_file()] 
            extractImages(self.targetDirPath,'tmp_video_images')
        else:
            QMessageBox.about(self,"Info",
                                     'Please select the video first !!!')
        ImagesList = glob.glob('tmp_video_images/*.jpg')
        if len(ImagesList) > 0:
            self.progress = QProgressDialog('Processing the Data', 'Done', 0, 100, self)
            self.progress.setWindowModality(Qt.WindowModal)
            self.progress.setGeometry(200, 150, 200, 30) 
            self.progress.setCancelButton(None)
            self.progress.show()
            self.progress.setValue(0)
            if os.path.isdir('runs'):
                shutil.rmtree('runs')
            detecteionOutput = subprocess.check_output(["python3", "detection_framework/detect.py","--weights", "best.pt", "--img", "640", "--conf", "0.2", "--source", 'tmp_video_images/'], universal_newlines=True)
            self.progress.setValue(100)      
        else:
            QMessageBox.about(self,"Info",
                                     'Please select the video first !!!')
                
    def startProcessVideo(self):
        self.videoProcessing = True
        with open('detections.json') as json_file:
            detection_results_data  = json.load(json_file)
        ImagesList = glob.glob('tmp_video_images/*.jpg')
        if len(ImagesList) > 0:
            for imagepath in ImagesList:
                if (self.videoProcessing == True):
                    OutputImage = os.path.dirname(os.path.realpath(__file__))+'/runs/detect/exp/'+os.path.basename(imagepath)

                    self.detectionspeedline.setText(" {:0.3f}".format(detection_results_data[os.path.basename(imagepath)]['detection_time']))
                    if len(detection_results_data[os.path.basename(imagepath)]['confidence']) > 0:
                        self.probabilityline.setText(" {:0.3f}".format(max(detection_results_data[os.path.basename(imagepath)]['confidence'])))
                    self.fpsrateline.setText(" {}".format(detection_results_data['FPS']))

                    testimage = QPixmap(imagepath)
                    self.originalVideo.setPixmap(testimage)

                    yoloOutputImage = QPixmap(OutputImage)
                    self.yoloDetectImage.setPixmap(yoloOutputImage)
                    QApplication.processEvents()
                    time.sleep(2)
                    
                else:
                    break
        else:
            QMessageBox.about(self,"Info",
                                     'Please select the video first !!!')

    def stopProcessVideo(self):
        if (self.videoProcessing == True):
            self.videoProcessing = False
            QApplication.processEvents()


class WidgetGallery(QWidget):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox)
        mainLayout.addWidget(self.topRightGroupBox)
        mainLayout.addWidget(self.bottomRightGroupBox)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Styles")

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox()

        modelPushButton = QPushButton("Burn Model on Yolo V5")
        modelPushButton.setDefault(True)

        layout = QVBoxLayout()
        layout.addWidget(modelPushButton)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox()

        self.imagesPushButton = QPushButton("Images")
        self.imagesPushButton.setDefault(True)

        self.videoPushButton = QPushButton("Video")
        self.videoPushButton.setDefault(True)

        layout = QHBoxLayout()
        layout.addWidget(self.imagesPushButton)
        layout.addWidget(self.videoPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)    

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox()

        self.closePushButton = QPushButton("Close")
        self.closePushButton.setDefault(True)

        layout = QHBoxLayout()
        layout.addWidget(self.closePushButton)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.startMainWindow()

    def startMainWindow(self):
        self.Window = WidgetGallery(self)
        self.setCentralWidget(self.Window)
        self.Window.imagesPushButton.clicked.connect(self.startImageWindow)
        self.Window.videoPushButton.clicked.connect(self.startVideoWindow)
        self.Window.closePushButton.clicked.connect(self.closeEvent)
        self.show()

    def startImageWindow(self):
        self.Window = ImageWindow(self)
        self.startwindow("Image Window")

    def startVideoWindow(self):
        self.Window = VideoWindow(self)
        self.startwindow("Video Window")

    def startwindow(self, Win_Title):
        self.setWindowTitle(Win_Title)
        self.setCentralWidget(self.Window)
        self.Window.closePushButton.clicked.connect(self.closeEvent)
        self.Window.backPushButton.clicked.connect(self.startMainWindow)
        self.show()


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit?',
                                     'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if not type(event) == bool:
                event.accept()
            else:
                sys.exit()
        else:
            if not type(event) == bool:
                event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle('Macintosh')
    gallery = MainWindow()
    sys.exit(app.exec_()) 
