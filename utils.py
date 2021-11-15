from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import os
import cv2

def createleftbuttons(self):
    self.topLeftGroupBox = QGroupBox()
    self.selectFileDir = QPushButton("Select Source")
    self.selectFileDir.setDefault(True)
    self.selectFileDir.clicked.connect(self.openDirDialog)

    layout = QVBoxLayout()
    layout.addWidget(self.selectFileDir)
    layout.addStretch(1)
    self.topLeftGroupBox.setLayout(layout)    

def createrightbuttons(self):
    self.topRightGroupBox = QGroupBox()
    self.refreshPushButton = QPushButton("Refresh")
    self.refreshPushButton.setDefault(True)
    self.backPushButton = QPushButton("Back")
    self.backPushButton.setDefault(True)
    self.closePushButton = QPushButton("Close")
    self.closePushButton.setDefault(True)
    layout = QHBoxLayout()
    layout.addWidget(self.refreshPushButton)
    layout.addWidget(self.backPushButton)
    layout.addWidget(self.closePushButton)
    layout.addStretch(1)
    self.topRightGroupBox.setLayout(layout)   

def createleftbottombox(self,window_type):
    self.bottomLeftGroupBox = QGroupBox()
    self.imageProcessing = False
    layout = QVBoxLayout()

    startPushButton = QPushButton("Start")
    startPushButton.setDefault(True)
    layout.addWidget(startPushButton)

    stopPushButton = QPushButton("Stop")
    stopPushButton.setDefault(True)
    layout.addWidget(stopPushButton)

    if(window_type == "image"):
        prevPushButton = QPushButton("Prev")
        prevPushButton.setDefault(True)
        layout.addWidget(prevPushButton)

        nextPushButton = QPushButton("Next")
        nextPushButton.setDefault(True)
        layout.addWidget(nextPushButton)

        startPushButton.clicked.connect(self.startProcessImages)
        stopPushButton.clicked.connect(self.stopProcessImages)

    else:
        startPushButton.clicked.connect(self.startProcessVideo)
        stopPushButton.clicked.connect(self.stopProcessVideo)

    layout.addStretch(1)
    self.bottomLeftGroupBox.setLayout(layout)

def createletflastbox(self):
    self.lastLeftGroupBox = QGroupBox()    
    
    labelFps = QLabel("FPS :", self)
    self.fpsrateline = QLineEdit('')

    labelProb = QLabel("Probability :", self)
    self.probabilityline = QLineEdit('')

    labeldetection = QLabel("Detection Time :", self)
    self.detectionspeedline = QLineEdit('')
        
    layout = QVBoxLayout()
    layout.addWidget(labelFps)
    layout.addWidget(self.fpsrateline)
    layout.addWidget(labelProb)
    layout.addWidget(self.probabilityline)
    layout.addWidget(labeldetection)
    layout.addWidget(self.detectionspeedline)
    layout.addStretch(1)
    self.lastLeftGroupBox.setLayout(layout)

def extractImages(targetDirPath, pathOut):
    video_name = os.path.basename(targetDirPath[0])
    vidcap = cv2.VideoCapture(targetDirPath[0])
    success = True
    count = 0
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
        success,image = vidcap.read()
        if success:
            cv2.imwrite("{}/{}_frame{}.jpg".format(pathOut, video_name, count), image)
            my_image = "{}/{}_frame{}.jpg".format(pathOut, video_name, count)
            try:
                im = Image.open(my_image)
                imResize = im.resize((640, 640), Image.ANTIALIAS)
                imResize.save(pathOut + "/" + video_name + "_frame{}.jpg".format(count), "JPEG")            
            except:
                pass
            count = count + 1



