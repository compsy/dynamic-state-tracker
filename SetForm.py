import PyQt5
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QButtonGroup)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QLineEdit, QGridLayout, QComboBox
import sys
import MediaPlayer
import Form
class SetFormWindow(QMainWindow):
    def __init__(self, parent=None, form_list = None):
        super(SetFormWindow, self).__init__(parent)
        self.parent = parent
        self.video_dir = None
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
        # Create playVideoButton and link to function play_video
        self.addButton = QPushButton("Add", self)
        self.addButton.setEnabled(True)
        self.addButton.clicked.connect(self.step_add)
        
        # Create setQuestionsButton and link to function set_questions
        self.removeButton = QPushButton("Remove", self)
        self.removeButton.setEnabled(True)
        self.removeButton.clicked.connect(self.remove_question)
  
        self.submitButton = QPushButton("Submit", self)
        self.submitButton.setEnabled(True)
        self.submitButton.clicked.connect(self.export_form)
        

        
        self.layout.addWidget(self.addButton,0,0)
        self.layout.addWidget(self.removeButton,0,1)
        self.layout.addWidget(self.submitButton,0,2)
        
    def step_add(self):
        self.add_question("Not set")
        
        

            
    def initalize_questions(self):
        
        for q in self.form_list:
            self.add_question(q.get_question(),1)
            
    
    
    def add_question(self, text = None, type = 0):
        field = QLineEdit(self)
        if(not text):
            field.setText("Not set")
            print ("no text set")
        else:
            field.setText(text)
        self.question_fields.append(field)
        self.number_of_fields = self.number_of_fields+1
        self.layout.addWidget(field,self.number_of_fields,0)
        

    def remove_question(self):
        if(self.number_of_fields == 1):
            print("You cannot have 0 questions")
            return
        field_to_remove = self.question_fields.pop()
        field_to_remove.deleteLater()
        self.layout.removeWidget(field_to_remove)
        self.number_of_fields = self.number_of_fields-1

    def how_many_questions(self):
        print ( len(self.question_fields))
    
    def export_form(self):
        self.new_form_list = list()
        for i in range(0, len(self.question_fields)):
            newFormComponent = Form.Form()
            newFormComponent.set_question(self.question_fields[i].text())
            self.new_form_list.append(newFormComponent)
        

        self.parent.import_form(self.new_form_list)
        self.close()

       
    