import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QButtonGroup)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QLineEdit, QGridLayout, QComboBox
import sys
import MediaPlayer
import Form
import MultiLanguage
class FormWindow(QMainWindow):
    def __init__(self, parent=None, form_list = None):
        super(FormWindow, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Dynamic State Tracker 2.0")

        self.form_list = form_list
        self.question_fields = list()

        self.number_of_fields = 0

        self.layout = QGridLayout()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        self.initalize_questions()
        self.initalize_buttons()
       
        
    def initalize_buttons(self):
        '''
            Initalizes the submit button and links it to the submit function.
        '''
        self.submitButton = QPushButton(self.parent.MultiLang.find_correct_word("Submit"), self)
        self.submitButton.setEnabled(True)
        self.submitButton.clicked.connect(self.submit_form)

        self.layout.addWidget(self.submitButton,0,0)
        
    def initalize_questions(self):
        '''
            For every questions in the form, add an answer field.
        '''
        for q in self.form_list:
            self.add_answer(q.get_question(),1)
            
    
    
    def add_answer(self, text = None, type = 0):
        '''
            Adds a question into the window, if there is no text provided the question is set to "Failed to load.". Also inserts an answer box for each question.
        '''
        if(text == None):
            question = QLabel("Failed to load.")
        else:
            question = QLabel(text)
        field = QLineEdit(self)
        field.setText("")

        self.question_fields.append(field)
        self.number_of_fields = self.number_of_fields+1
        self.layout.addWidget(question,self.number_of_fields,0)
        self.layout.addWidget(field,self.number_of_fields,1)
        
    
    def submit_form(self):
        '''
            Opens the player and sends it the answered questions as a list.
        '''
        self.answered_form = list()
        for i in range(0, len(self.question_fields)):
            newFormComponent = Form.Form()
            newFormComponent.set_question(self.form_list[i].get_question())
            newFormComponent.set_data(self.question_fields[i].text())
            self.answered_form.append(newFormComponent)

        self.parent.video_player(self.answered_form)
        self.close()
   
    
       
    