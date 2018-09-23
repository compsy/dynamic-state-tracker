import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
import sys
import MediaPlayer
import SetQuestions
import Review
import Question
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        # Create DST title label
        titleLabel = QLabel("DST 2.0", self)
        titleLabel.move(50,25)
        titleLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        
        # Initalize all buttons on main menu
        self.initalize_buttons()
   
   
        # Initalize Questions list
        self.questions = list()
        self.time = 1000
        
        # add fake data for testing.
        test_question = Question.Question()
        test_question.set_question("text123")
        self.questions.append(test_question)
        
        test_question = Question.Question()
        test_question.set_question("text125")
        self.questions.append(test_question)
        self.questions.append(test_question)
        self.questions.append(test_question)
    def initalize_buttons(self):
        # Create playVideoButton and link to function play_video
        self.playVideoButton = QPushButton("Play Video", self)
        self.playVideoButton.move(50,80)
        self.playVideoButton.setEnabled(True)
        self.playVideoButton.clicked.connect(self.play_video)

        # Create setQuestionsButton and link to function set_questions
        self.setQuestionsButton = QPushButton("Set Questions", self)
        self.setQuestionsButton.move(50,130)
        self.setQuestionsButton.setEnabled(True)
        self.setQuestionsButton.clicked.connect(self.set_questions)

        # Create reviewButton and link to function review
        self.reviewButton = QPushButton("Review", self)
        self.reviewButton.move(50,180)
        self.reviewButton.setEnabled(True)
        self.reviewButton.clicked.connect(self.review)
    
    
    def play_video(self):
        player = MediaPlayer.MediaPlayer(self, self.questions, self.time)
        player.show()
        
    def set_questions(self):
        window = SetQuestions.QuestionsWindow(self, self.questions)
        window.show()
    def import_questions(self, new_questions, new_time):
        self.questions = new_questions
        try:
            self.time = int(new_time)
        except:
            print("invalid time selected, set to default of 1 second")
            self.time = 1000
        
    def review(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "","All Files (*);;Python Files (*.py)")
        if fileName:
            print(fileName)
            window = Review.ReviewWindow(self, fileName)
            window.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow= MainWindow()
    mainWindow.resize(200, 250)
    mainWindow.show()
    sys.exit(app.exec_())