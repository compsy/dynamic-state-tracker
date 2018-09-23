import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QButtonGroup)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QLineEdit, QGridLayout, QComboBox
import sys
import MediaPlayer
import Question
class QuestionsWindow(QMainWindow):
    def __init__(self, parent=None, current_questions = None):
        super(QuestionsWindow, self).__init__(parent)
        self.parent = parent
        self.questions = current_questions
        self.question_fields = list()
        self.combo_box_list = list()

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
            if q.get_type() == "Slider":
                self.add_question(q.get_question(),0)
            elif q.get_type() == "Binary":
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
        
        if(self.number_of_fields == 1):
            self.timeBox = QLineEdit("1000")
            self.layout.addWidget(self.timeBox,self.number_of_fields,2)

        self.add_combo_box(type)
 
    def add_combo_box(self, type):
        comboBox = QComboBox(self)
        
        comboBox.addItem("Slider")
        comboBox.addItem("Binary")

        comboBox.setCurrentIndex(type)

        
        self.layout.addWidget(comboBox, self.number_of_fields, 1)
        self.combo_box_list.append(comboBox)
        
    def remove_question(self):
        if(self.number_of_fields == 1):
            print("You cannot have 0 questions")
            return
        field_to_remove = self.question_fields.pop()
        field_to_remove.deleteLater()
        self.layout.removeWidget(field_to_remove)
        self.number_of_fields = self.number_of_fields-1
        
        combo_to_remove = self.combo_box_list.pop()
        self.layout.removeWidget(combo_to_remove)
        combo_to_remove.deleteLater()
        
        
    def how_many_questions(self):
        print ( len(self.question_fields))
    
    def export_questions(self):
        self.new_questions = list()
        for i in range(0, len(self.question_fields)):
            newQuestion = Question.Question()
            newQuestion.set_question(self.question_fields[i].text())
            newQuestion.set_type(self.combo_box_list[i].currentText())
            self.new_questions.append(newQuestion)
        

        self.parent.import_questions(self.new_questions, self.timeBox.text())
        self.close()

       
    