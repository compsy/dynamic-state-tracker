
from PyQt5.QtCore import QDir, Qt, QUrl, QThread, QRunnable, QThreadPool, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QGridLayout, QLineEdit
from PyQt5.QtGui import QIcon

import sys
import threading
import time
import json
import Form

from pynput.mouse import Controller

class MediaPlayer(QMainWindow):

    def __init__(self, parent=None, questions = None, time = None, answered_form = None):
        super(MediaPlayer, self).__init__(parent)
        self.questions = questions 
        self.answered_form = answered_form
        self.mouse = Controller()
        
  
        self.time = time
        self.setWindowTitle("Dynamic State Tracker 2.0") 
        #self.resize(500, 800)
        self.showMaximized()
        
        print ("Starting player!")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        
        # create play button
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        
        # Create slider for video position
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        # Create label to output errors
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

        layout = QGridLayout()
        layout.setRowStretch(0,2)
        layout.setVerticalSpacing(1)
        layout.addWidget(videoWidget,0,0)
        layout.addLayout(controlLayout,1,0)

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
                self.slider.setMouseTracking(True)
                self.type = "one"
                
                self.question_text = QLabel(self.questions[0].get_question())
                layout.addWidget(self.question_text, 3, 0, Qt.AlignCenter)
                
                #Create layouts to place slider inside
                sliderLayout = QHBoxLayout()
                sliderLayout.setContentsMargins(0, 0, 0, 0)
                
                sliderLayout.addWidget(self.slider)
                sliderLayout.addWidget(self.percent_text)
               
                
                
                
                
                layout.addLayout(sliderLayout,4,0)
        elif(len(self.questions) > 1):
                self.type = "multi"
        
        
        #Add timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.record)
        
        # Add error label to layout
        layout.addWidget(self.errorLabel)

        
 
    def closeEvent(self, event):
        print ("Closing")
        self.timer.stop()
        self.close()
        
    def value_change(self):
        size = str(self.slider.value())
        self.percent_text.setText(size)
        
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            print (fileName)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.video_dir = fileName

    def exitCall(self):
        print("Exiting!")
        sys.exit(app.exec_())

            
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
            
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
                
            self.timer.start(self.time)
        elif self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            print("video ended!")
            self.timer.stop()
            save_window = SaveFileWindow(self)
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
            self.timer.stop()

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


        
    def record(self):
         if self.type == "one":
                size_x = self.slider.geometry().width()
                #print(str(self.mouse.position[0]) + " / " + str(size_x))
                new_value = int(100*self.mouse.position[0]/size_x)
                self.slider.setValue(new_value)
                self.questions[0].add_data(new_value)
         elif self.type == "multi":
                self.timer.stop()
                popup = MultiQuestionPopUP(self)
                #print("recrding pop up!")
        
class MultiQuestionPopUP(QMainWindow):
    def __init__(self, parent=None):
        super(MultiQuestionPopUP, self).__init__(parent)
        
        self.parent = parent
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        self.temp_label = QLabel("Multi Questions not yet implemented!")
        self.layout.addWidget(self.temp_label, 0, 0)
        
        self.show()
        self.parent.close()
        
class SaveFileWindow(QMainWindow):
     def __init__(self, parent=None):
        super(SaveFileWindow, self).__init__(parent)

        
        
        self.parent = parent
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        self.file_name_box = QLineEdit("File name here")
        self.layout.addWidget(self.file_name_box, 0, 0)
        
        self.save_button = QPushButton("Save file")
        self.save_button.clicked.connect(self.save_file)
        self.layout.addWidget(self.save_button, 0, 1)
        
        self.show()

     def save_file(self):
        file_name = self.file_name_box.text()
        
        try:
            f = open("saves/" + file_name + ".txt", "w+")
            f.write(self.parent.video_dir + "//")
            f.write(str(self.parent.time) + "//")
            
            for q in self.parent.questions:
                save_string = q.get_question() + " - " + json.dumps(q.get_data())
                f.write(save_string + "//")
            
            f.write("~")
                 
            
            for q in self.parent.answered_form:
                first_text = str(q.get_question())
                second_text = str(q.get_data())
                save_string = first_text + " - " + second_text
                f.write(save_string + "//")
            
            
            f.close()
            print("Sucessfully saved!")
            
        except:
            print("Saving failed!")
        
        exit_window = EndWindow(self, "Goodbye!")
    
class EndWindow(QMainWindow):
    def __init__(self, parent = None, text = None):
        super(EndWindow, self).__init__(parent)
        self.parent = parent
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        self.label = QLabel(text)
        self.accept_button = QPushButton("Finish")
        self.accept_button.clicked.connect(self.accept)
        
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.accept_button, 1, 0)
        
        self.show()
    def accept(self):
        self.parent.parent.close()
        self.parent.close()
        self.close()