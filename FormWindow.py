import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QButtonGroup)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QLineEdit, QGridLayout, QComboBox
import sys
import MediaPlayer
import Form
class FormWindow(QMainWindow):
    def __init__(self, parent=None, form_list = None):
        super(FormWindow, self).__init__(parent)
        self.parent = parent
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
        self.submitButton = QPushButton("Submit", self)
        self.submitButton.setEnabled(True)
        self.submitButton.clicked.connect(self.submit_form)

        self.layout.addWidget(self.submitButton,0,0)
        
    def step_add(self):
        self.add_question("Not set")
        
    def initalize_questions(self):
        
        for q in self.form_list:
            self.add_question(q.get_question(),1)
            
    
    
    def add_question(self, text = None, type = 0):
        question = QLabel(text)
        field = QLineEdit(self)
        field.setText("answer..")

        self.question_fields.append(field)
        self.number_of_fields = self.number_of_fields+1
        self.layout.addWidget(question,self.number_of_fields,0)
        self.layout.addWidget(field,self.number_of_fields,1)
        

    def how_many_questions(self):
        print ( len(self.question_fields))
    
    def submit_form(self):
        self.answered_form = list()
        for i in range(0, len(self.question_fields)):
            newFormComponent = Form.Form()
            newFormComponent.set_question(self.form_list[i].get_question())
            newFormComponent.set_data(self.question_fields[i].text())
            self.answered_form.append(newFormComponent)

        #self.parent.import_form(self.new_form_list)
        self.parent.video_player(self.answered_form)
        self.close()
   
    
       
    