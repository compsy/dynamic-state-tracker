import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
import sys
import MediaPlayer
import SetQuestions
import Review
import Question
import SetForm
import Form
import FormWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        # Create DST title label
        titleLabel = QLabel("DST 2.0", self)
        titleLabel.move(50,25)
        titleLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        
        # Initalize all buttons on main menu
        self.initalize_buttons()
   
        # Initalize author text
        self.initalize_tag()
   
        # Initalise time
        self.time = 1000
        
        # Tries to load form and question formats, else it creates a new blank list.
        self.load_from_file()

        
    def initalize_tag(self):
        titleLabel = QLabel("By Oliver Holder", self)
        titleLabel.move(90,270)
            
    def initalize_buttons(self):
        # Create playVideoButton and link to function play_video
        self.playVideoButton = QPushButton("Play Video", self)
        self.playVideoButton.move(50,80)
        self.playVideoButton.setEnabled(True)
        self.playVideoButton.clicked.connect(self.open_question_form)

        # Create setQuestionsButton and link to function set_questions
        self.setQuestionsButton = QPushButton("Set Questions", self)
        self.setQuestionsButton.move(50,130)
        self.setQuestionsButton.setEnabled(True)
        self.setQuestionsButton.clicked.connect(self.set_questions)
        
        # Create setFormButton and link to function set_form
        self.setFormButton = QPushButton("Set Form", self)
        self.setFormButton.move(50,180)
        self.setFormButton.setEnabled(True)
        self.setFormButton.clicked.connect(self.set_form)

        
        # Create reviewButton and link to function review
        self.reviewButton = QPushButton("Review", self)
        self.reviewButton.move(50,230)
        self.reviewButton.setEnabled(True)
        self.reviewButton.clicked.connect(self.review)
    
    def open_question_form(self):
        form_window = FormWindow.FormWindow(self, self.form_list)
        form_window.show()
    
    def video_player(self, answered_form):
        player = MediaPlayer.MediaPlayer(self, self.questions, self.time, answered_form)
        player.show()
        
    def set_questions(self):
        window = SetQuestions.QuestionsWindow(self, self.questions, self.time)
        window.show()
    def import_questions(self, new_questions, new_time):
        self.questions = new_questions
        try:
            self.time = int(new_time)
        except:
            print("invalid time selected, set to default of 1 second")
            self.time = 1000
            

        try:
            f = open("saves/Questions_layout/questions.txt", "w+")
            for q in self.questions:
                f.write(q.get_question() + "//")
            f.write("~" + str(new_time))
            f.close()
            print("Sucessfully saved!")
        
        except:
            print("Saving failed!")
    
            
    def set_form(self):
        window = SetForm.SetFormWindow(self, self.form_list)
        window.show()
        
    
    def review(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "saves","All Files (*);;Python Files (*.py)")
        if fileName:
            print(fileName)
            window = Review.ReviewWindow(self, fileName)
            window.show()

    def import_form(self, new_form_list):
        self.form_list = new_form_list

        try:
            f = open("saves/Form_layout/form.txt", "w+")
            for q in self.form_list:
                f.write(q.get_question() + "//")
            f.close()
            print("Sucessfully saved!")
        
        except:
            print("Saving failed!")
    

    def load_from_file(self):
        new_form_list = list()

        f = open("saves/Form_layout/form.txt", "r")
        with f:
            data = f.read()
            segments = data.split("//")
            for q_text in segments:
                if (q_text != ""):
                    newFormComponent = Form.Form()
                    newFormComponent.set_question(q_text)
                    new_form_list.append(newFormComponent)
        
        
        self.form_list = new_form_list
        
        new_questions_list = list()

        f = open("saves/Questions_layout/questions.txt", "r")
        with f:
            data = f.read()
            segments1 = data.split("~")
            segments2 = segments1[0].split("//")
            for q_text in segments2:
                if (q_text != ""):
                    newFormComponent = Question.Question()
                    newFormComponent.set_question(q_text)
                    new_questions_list.append(newFormComponent)
                        
        self.questions = new_questions_list
        self.time = int(segments1[1])

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow= MainWindow()
    mainWindow.resize(200, 300)
    mainWindow.show()
    sys.exit(app.exec_())