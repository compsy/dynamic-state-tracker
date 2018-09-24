
from PyQt5.QtCore import QDir, Qt, QUrl, QThread, QRunnable, QThreadPool
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QGridLayout
from PyQt5.QtGui import QIcon
import sys
import threading
import time

class MediaPlayer(QMainWindow):

    def __init__(self, parent=None, questions = None, time = None):
        super(MediaPlayer, self).__init__(parent)
        self.questions = questions 
        self.time = time

        self.setWindowTitle("Dynamic State Tracker 2.0") 
        self.resize(500, 800)
        print ("Starting player!")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        
    
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        


        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        
        
        # Create slider and label
           
        ## ADD INPUT METHOD DEPENDING ON AMOUNT OF QUESTIONS AND TIME

        
        if(len(self.questions) == 1):
                self.percent_text = QLabel("0")
                self.slider = QSlider(Qt.Horizontal)
                self.slider.setFocusPolicy(Qt.StrongFocus)
                self.slider.setTickPosition(QSlider.TicksBothSides)
                self.slider.setTickInterval(10)
                self.slider.setSingleStep(1)      
                self.slider.valueChanged.connect(self.value_change)
                self.type = "one"
                
                self.question_text = QLabel(self.questions[0].get_question())
                
                #Create layouts to place slider inside
                sliderLayout = QHBoxLayout()
                sliderLayout.setContentsMargins(0, 0, 0, 0)
                sliderLayout.addWidget(self.question_text)
                sliderLayout.addWidget(self.slider)
                sliderLayout.addWidget(self.percent_text)
               
                
                
                
                
                layout.addLayout(sliderLayout)
        elif(len(self.questions) > 1):
                self.type = "multi"
        
        # Add error label to layout
        layout.addWidget(self.errorLabel)

    def value_change(self):
        size = str(self.slider.value())
        self.percent_text.setText(size)
        
        
        
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        print("Exiting!")
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
            self.start_recording()
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
            
    def start_recording(self):
        self.p = ProcessRunnable(target=self.record())
        self.p.start()
        
    def record(self):
         if self.type == "one":
                print("recrding slider!")
         elif self.type == "multi":
                print("recrding pop up!")
        
class ProcessRunnable(QRunnable):
    def __init__(self, target, args = None):
        QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        if self.args == None:
            self.t()
        else:
            self.t(*self.args)

    def start(self):
        QThreadPool.globalInstance().start(self)