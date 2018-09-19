import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QButtonGroup)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QLineEdit, QGridLayout, QRadioButton
import sys
import MediaPlayer
import Question
class QuestionsWindow(QMainWindow):
    def __init__(self, parent=None, current_questions = None):
        super(QuestionsWindow, self).__init__(parent)
        self.parent = parent
        self.questions = current_questions
        self.question_fields = list()
        self.radio_b1_list = list()
        self.radio_b2_list = list()

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
        self.addButton.move(0,10)
        self.addButton.setEnabled(True)
        self.addButton.clicked.connect(self.step_add)
        
        # Create setQuestionsButton and link to function set_questions
        self.removeButton = QPushButton("Remove", self)
        self.removeButton.move(100,10)
        self.removeButton.setEnabled(True)
        self.removeButton.clicked.connect(self.remove_question)
  
        self.submitButton = QPushButton("Submit", self)
        self.submitButton.move(100,10)
        self.submitButton.setEnabled(True)
        self.submitButton.clicked.connect(self.export_questions)
        
        
        self.layout.addWidget(self.addButton,0,0)
        self.layout.addWidget(self.removeButton,0,1)
        self.layout.addWidget(self.submitButton,0,2)
        
    def step_add(self):
        self.add_question("Not set")
        
    def initalize_questions(self):
        for q in self.questions:
            self.add_question(q.get_question())
            
    
    
    def add_question(self, text = None):
        # TEXT FIELD
        field = QLineEdit(self)
        if(not text):
            field.setText("Not set")
            print ("no text set")
        else:
            field.setText(text)
        self.question_fields.append(field)
        self.number_of_fields = self.number_of_fields+1
        self.layout.addWidget(field,self.number_of_fields,0)

        # RADIO BUTTONS

        
        b1 = QRadioButton( "Slider")
        b1.setChecked(True)
        self.layout.addWidget(b1, self.number_of_fields, 1)
        self.radio_b1_list.append(b1)
        
        b2 = QRadioButton("Binary")
        b2.setChecked(False)
        self.layout.addWidget(b2, self.number_of_fields, 2) 
        self.radio_b2_list.append(b2)

        
        radio_holder = QButtonGroup()
        radio_holder.addButton(b1, 1)
        radio_holder.addButton(b2, 2)
        #b1.toggled.connect(lambda:self.turn_of_radio(b1,b2))
        
        #b2.toggled.connect(lambda:self.turn_of_radio(b2,b1))
        
    def remove_question(self):
        field_to_remove = self.question_fields.pop()
        field_to_remove.deleteLater()
        self.layout.removeWidget(field_to_remove)
        self.number_of_fields = self.number_of_fields-1
        self.how_many_questions()
        
        radio_to_remove = self.radio_b1_list.pop()
        self.layout.removeWidget(radio_to_remove)
        radio_to_remove.deleteLater()
        
        radio_to_remove = self.radio_b2_list.pop()
        self.layout.removeWidget(radio_to_remove)
        radio_to_remove.deleteLater()
        
    def how_many_questions(self):
        print ( len(self.question_fields))
    
    def export_questions(self):
        self.new_questions = list()
        for f in self.question_fields:
            newQuestion = Question.Question()
            newQuestion.set_question(f.text())
            self.new_questions.append(newQuestion)
        
        self.parent.import_questions(self.new_questions)
        self.close()
        
    def turn_of_radio(self, on, off):
        #on.setChecked(True)
        off.setChecked(False)
       
    