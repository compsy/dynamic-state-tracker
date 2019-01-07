import PyQt5 
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QComboBox
import sys
import MediaPlayer
import SetQuestions
import Review
import Question
import SetForm
import Form
import FormWindow
import MultiLanguage

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("DST")
        
        self.version = "2.3"
        print("Application starting... this may take a few seconds")
        
        
        # Create DST title label
        titleLabel = QLabel("DST " + self.version, self)
        titleLabel.move(50,25)
        titleLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        
        # Create MultiLanguage instance
        self.MultiLang = MultiLanguage.MultiLanguage("English")
        
        # Initalize all buttons on main menu
        self.initalize_buttons()
   
        # Initalize author text
        self.initalize_tag()
   
        # Initalise time
        self.time = 1000
        
        # Tries to load form and question formats, else it creates a new blank list.
        self.load_from_file()
          
        # Add Icon 
        self.setWindowIcon(QtGui.QIcon('logo.png'))
          
    def change_language(self, widget):
        self.MultiLang.set_language(self.languageBox.currentText())
        
        # reload all text in main window
        self.playVideoButton.setText(self.MultiLang.find_correct_word("Start Video"))
        self.setQuestionsButton.setText(self.MultiLang.find_correct_word("Set items"))
        self.setFormButton.setText(self.MultiLang.find_correct_word("Basic questions"))
        self.reviewButton.setText(self.MultiLang.find_correct_word("Show result"))
        
    def initalize_tag(self):
        titleLabel = QLabel("By Oliver Holder, \nRuud den Hartigh", self)
        titleLabel.move(80,320)
            
    def initalize_buttons(self):
        # Create playVideoButton and link to function open questions form
        self.playVideoButton = QPushButton(self.MultiLang.find_correct_word("Start Video"), self)
        self.playVideoButton.move(15,80)
        self.playVideoButton.setEnabled(True)
        self.playVideoButton.clicked.connect(self.open_question_form)
        self.playVideoButton.setStyleSheet ('font: bold 14px;min-width: 10em;padding: 0px;') 

        # Create setQuestionsButton and link to function set_questions
        self.setQuestionsButton = QPushButton(self.MultiLang.find_correct_word("Set items"), self)
        self.setQuestionsButton.move(15,130)
        self.setQuestionsButton.setEnabled(True)
        self.setQuestionsButton.clicked.connect(self.set_questions)
        self.setQuestionsButton.setStyleSheet ('font: bold 14px;min-width: 10em;padding: 0px;') 
        
        # Create setFormButton and link to function set_form
        self.setFormButton = QPushButton(self.MultiLang.find_correct_word("Basic questions"), self)
        self.setFormButton.move(15,180)
        self.setFormButton.setEnabled(True)
        self.setFormButton.clicked.connect(self.set_form)
        self.setFormButton.setStyleSheet ('font: bold 14px;min-width: 10em;padding: 0px;') 

        # Create reviewButton and link to function review
        self.reviewButton = QPushButton(self.MultiLang.find_correct_word("Show result"), self)
        self.reviewButton.move(15,230)
        self.reviewButton.setEnabled(True)
        self.reviewButton.clicked.connect(self.review)
        self.reviewButton.setStyleSheet ('font: bold 14px;min-width: 10em;padding: 0px;') 
        
        # Create language setting
        self.languageBox = QComboBox(self)
        
        self.languageBox.addItem("English")
        self.languageBox.addItem("Nederlands")
        self.languageBox.addItem("Français")
        self.languageBox.addItem("Español")
        self.languageBox.addItem("Deutsche")
        self.languageBox.setCurrentIndex(0)
        
        self.languageBox.move(50,280)
        self.languageBox.currentIndexChanged.connect(self.change_language)
    
    def open_question_form(self):
        '''
            This function either asks the form questions, for forwards straight to the video player if there are no form questions.
        '''
        if(len(self.form_list) == 0):
            self.video_player(list())
        else:
            form_window = FormWindow.FormWindow(self, self.form_list)
            form_window.show()
    
    def video_player(self, answered_form):
        player = MediaPlayer.MediaPlayer(self, self.questions, self.time, answered_form)
        player.show()
        
    def set_questions(self):
        window = SetQuestions.QuestionsWindow(self, self.questions, self.time)
        window.show()
        
    def import_questions(self, new_questions, new_time):
        '''
            This function saves questions after they have been changed in the "set questions" window. 
            It saves both to the current questions in the program and to the file that holds the questions.
        '''
        self.questions = new_questions
        try:
            self.time = int(new_time)
        except:
            print("invalid time selected, set to default of 1 second")
            self.time = 1000
            
        try:
            f = open("saves/Questions_layout/questions.txt", "w+")
            for q in self.questions:
                f.write(q.get_question() + "|" + q.get_min() + "|" + q.get_max() + "//")
            f.write("~" + str(new_time))
            f.close()
            print("Sucessfully saved!")
        
        except:
            print("Saving failed!")
       
    def set_form(self):
        window = SetForm.SetFormWindow(self, self.form_list)
        window.show()
        
    def review(self):
        fileName, _ = QFileDialog.getOpenFileName(self,self.MultiLang.find_correct_word("Open File"), "saves","All Files (*);;Python Files (*.py)")
        if fileName:
            print(fileName)
            window = Review.ReviewWindow(self, fileName)
            window.show()

    def import_form(self, new_form_list):
        '''
            This function saves form questions after they have been set in the "set form" window.
            This function saves the form layout in both the program and the save file.
        '''
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
        '''
            This function loads both the form and question lists from their respective save files. If loading fails then they become empty.
            The form layout is loaded from 'saves/Form_layout/form.txt' and the questions from 'saves/Questions_layout/questions.txt'.
        '''
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
        self.time = 500
        
        try:
            f = open("saves/Questions_layout/questions.txt", "r")
            with f:
                data = f.read()
                segments1 = data.split("~")
                segments2 = segments1[0].split("//")
                for q_text in segments2:
                    if (q_text != ""):
                        q_split = q_text.split("|")
                        newQuesiton = Question.Question()
                        newQuesiton.set_question(q_split[0])
                        newQuesiton.set_min_max(q_split[1], q_split[2])
                        new_questions_list.append(newQuesiton)
                        
            self.questions = new_questions_list
            self.time = int(segments1[1])
        except: 
            print("Items load failed, set to none.")
            self.questions = list()
    
    

        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow= MainWindow()
    mainWindow.resize(200, 360)
    mainWindow.show()
    sys.exit(app.exec_())