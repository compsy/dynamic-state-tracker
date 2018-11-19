
from PyQt5.QtCore import QDir, Qt, QUrl, QThread, QRunnable, QThreadPool, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QGridLayout, QLineEdit
from PyQt5.QtGui import QIcon,QFont

import sys
import threading
import time
import json
import Form
import math

from pynput.mouse import Controller

import MultiLanguage

class MediaPlayer(QMainWindow):

    def __init__(self, parent=None, questions = None, time = None, answered_form = None):
        # Initalize self and variables
        super(MediaPlayer, self).__init__(parent)
        self.parent = parent
        self.questions = questions 
        self.answered_form = answered_form
        self.time = time
        self.setWindowTitle("Dynamic State Tracker 2.0")

        
        # Reset data in questions!
        for q in self.questions:
            q.reset_data()
            
        # Controller component is needed to track mouse while it is not clicked.
        self.mouse = Controller()
        
        # The player should be maximised! This is due to how the mouse tracking works.
        self.showMaximized()
        
        # Create media player and video widget.
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        # create play button
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        
        # Create slider for video position
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setStyleSheet("QSlider::handle:horizontal {background-color: grey; border: 1px solid #777; width 13px; margin-top: -3px; margin-bottom: -3px; border-radius: 2px;}")
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        
        # Create label for video position
        
        self.positionLabel = QLabel("0")
        newfont = QFont("Times", 20) 
        self.positionLabel.setFont(newfont)

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

        # Create save action
        saveAction = QAction(QIcon('save.png'), '&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.saveAndExit)
        
        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        fileMenu.addAction(saveAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.positionLabel)

        self.layout = QGridLayout()
        self.layout.setRowStretch(0,2)
        self.layout.setVerticalSpacing(1)
        self.layout.addWidget(videoWidget,0,0)
        self.layout.addLayout(controlLayout,1,0)

        # Set widget to contain window contents
        wid.setLayout(self.layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        
        ## ADD INPUT METHOD DEPENDING ON AMOUNT OF QUESTIONS AND TIME
        if(len(self.questions) == 1):
             self.create_single_mode()
        elif(len(self.questions) > 1):
                # Initalize type variable for later.
                self.type = "multi"    
        
        #Add timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.record)
        
        #For mouse smoothness
        self.auto_mouse_timer = QTimer()
        self.auto_mouse_timer.timeout.connect(self.update_mouse)
        
        # Add error label to layout
        self.layout.addWidget(self.errorLabel)

    def create_single_mode(self):
        ''' 
            This function is called when the program is in single question mode.
            It creates the slider, question and labels.
            It also sets type to 'one' (this is used later for recording)
        '''
       # Initalize slider, initalize type variable for later.
        self.percent_text = QLabel("0")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet("QSlider::handle:horizontal {background-color: blue; border: 1px solid #777; width 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;}")
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)      
        self.slider.valueChanged.connect(self.value_change)
        self.slider.setMouseTracking(True)
        self.type = "one"
        
        # Creates a label with the asked question, then adds it to the main layout.
        self.question_text = QLabel(self.questions[0].get_question())
        newfont = QFont("Times", 20, QFont.Bold) 
        self.question_text.setFont(newfont)
        self.layout.addWidget(self.question_text,3,0, Qt.AlignCenter)
        
        # Labels for the extremes
        #         old                  max_label = QLabel(self.parent.MultiLang.find_correct_word("Very much"))
        #         old                  min_label = QLabel(self.parent.MultiLang.find_correct_word("Not at all"))
        max_label = QLabel(self.questions[0].get_max())
        min_label = QLabel(self.questions[0].get_min())
        
        newfont = QFont("Times", 16, QFont.Bold) 
        max_label.setFont(newfont)
        min_label.setFont(newfont)
        textLayout = QHBoxLayout()
        textLayout.setContentsMargins(0, 0, 0 ,0)
        textLayout.addWidget(min_label,0, Qt.AlignLeft)
        textLayout.addWidget(max_label,0, Qt.AlignRight)
        self.layout.addLayout(textLayout, 5, 0)
        
        # Create layouts to place slider inside
        sliderLayout = QHBoxLayout()
        sliderLayout.setContentsMargins(0, 0, 0, 0)
        
        # Add slider and percent text to slider layout.
        sliderLayout.addWidget(self.slider)
        sliderLayout.addWidget(self.percent_text)
       
        # Add slider layout to the main window layout.
        self.layout.addLayout(sliderLayout,4,0)
    

 
    def closeEvent(self, event):
        print ("Closing")
        self.timer.stop()
        self.auto_mouse_timer.stop()
        self.close()
        
    def value_change(self):
        size = str(self.slider.value())
        self.percent_text.setText(size)
        
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            print ("Loading url: " + fileName)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            print ("Loading Qurl: " + str(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.video_dir = fileName

    def exitCall(self):
        print("Exiting!")
        self.close()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
            
    def mediaStateChanged(self, state):
        '''
            If media state is changed, this function is called.
            If the video is playing, the timer is started for recording input.
            If the video is paused, the timer is stopped.
            If the video is ended, open the save window and end the timer.
        '''
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            # set timer interval to self.time. This self.time is loaded from the setQuestions settings.    
            self.timer.start(self.time)
            self.auto_mouse_timer.start(50)
        elif self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            self.saveAndExit()
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.timer.stop()
            self.auto_mouse_timer.stop

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.positionLabel.setText(self.format_time(self.mediaPlayer.position()))

        
    def format_time(self, m_seconds):
        seconds = round(m_seconds/1000)
        mins = math.floor(seconds / 60) 
        reduced_seconds = seconds % 60
        if (reduced_seconds < 10):
            seconds_str = "0" + str(reduced_seconds)
        else:
            seconds_str = str(reduced_seconds)
        formated_time = str(mins) + ":" + seconds_str
        return formated_time
        
        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def update_mouse(self):
        if self.type == "one":
            size_x = self.slider.geometry().width()
            new_value = int(100*self.mouse.position[0]/size_x)
            self.slider.setValue(new_value)
        
    def record(self):
        '''
            This function performs the recording of input. If we are in single question mode, first the slider will update to the mouse, and then it will be recorded.
            If in multi-question mode, the 'MultiQuestionPopUP' class is used to record the input.
        '''
        if self.type == "one":
               size_x = self.slider.geometry().width()
               new_value = int(100*self.mouse.position[0]/size_x)
               self.slider.setValue(new_value)
               self.questions[0].add_data(new_value)
        elif self.type == "multi":
               self.timer.stop()
               popup = MultiQuestionPopUP(self)
               self.play() #Actually pauses, confusingly
        
    def saveAndExit(self):
        if(self.mediaPlayer.state() == QMediaPlayer.PlayingState):
            self.play() #Actually pauses.
        self.timer.stop()
        save_window = SaveFileWindow(self)
    
class MultiQuestionPopUP(QMainWindow):
    def __init__(self, parent=None):
        super(MultiQuestionPopUP, self).__init__(parent)
        self.setWindowTitle("Questions")
        self.parent = parent
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        # A list to hold all the sliders so we can reference back to them later on submit!
        self.slider_list= list()
        
        self.create_question_segments()
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button, len(self.slider_list)*2, 0) # the position here is multiplied by 2 because each question has a label and slider.
        
        self.show()
        
    def create_question_segments(self):
        '''
            Creates all the sliders and questions in the multi-question pop up.
        '''
        index = 0
        for q in self.parent.questions:
            question = QLabel(q.get_question())
            slider = QSlider(Qt.Horizontal)
            slider.setFocusPolicy(Qt.StrongFocus)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setTickInterval(10)
            slider.setSingleStep(1)      
            slider.setMouseTracking(True)
            self.slider_list.append(slider)
            
            last_value = q.last_value()
            if (last_value != None):     
                slider.setValue(last_value)

            self.layout.addWidget(question,index,0)
            self.layout.addWidget(slider, index+1, 0)
            
            index = index + 2
    def submit(self):
        '''
            Adds data to all the questions when user submits the multi-question window.
            Then restart the player and close this instance of multi-window.
        '''
        i = 0
        for q in self.parent.questions:
            q.add_data(self.slider_list[i].value())
            i = i + 1
        
        self.parent.play() #Restarts player
        self.close()
        
class SaveFileWindow(QMainWindow):
     def __init__(self, parent=None):
        super(SaveFileWindow, self).__init__(parent)
        self.setWindowTitle("Save file as:")
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
        '''
            Attempts to save file with the name in the text box.
            Saves both questions and form.
        '''
        file_name = self.file_name_box.text()
        
        # If there is no filename, then do nothing.
        if (file_name == ""):
            return 
        
        try:
            f = open("saves/" + file_name + ".txt", "w+")
            f.write(self.parent.video_dir + "//")
            f.write(str(self.parent.time) + "//")
            
            for q in self.parent.questions:
                save_string = q.get_question() + "|" + q.get_min() + "|" + q.get_max() + " - " + json.dumps(q.get_data())
                f.write(save_string + "//")
            
            # This is the symbol that splits the object.
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
        
        exit_window = EndWindow(self, self.parent.parent.MultiLang.find_correct_word("Thank you and goodbye!"))
    
class EndWindow(QMainWindow):
    def __init__(self, parent = None, text = None):
        super(EndWindow, self).__init__(parent)
        self.setWindowTitle("Exit window")
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
        '''
            Close video player, close save window, close self.
        '''
        self.parent.parent.close()
        self.parent.close()
        self.close()