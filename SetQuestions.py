import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QButtonGroup)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QLineEdit, QGridLayout, QComboBox
import sys
import MediaPlayer
import Question
class QuestionsWindow(QMainWindow):
    def __init__(self, parent=None, current_questions = None, current_time = None):
        super(QuestionsWindow, self).__init__(parent)
        self.setWindowTitle("Set Questions")
        # Save parent for later use in saving questions
        self.parent = parent
        
        # Store current questions from main program in local variable.
        self.questions = current_questions
        
        # Store current time period in local variable.
        self.current_time = current_time
        
        # Initalise widget lists for fields and combo boxes.
        self.question_fields = list()
        self.combo_box_list = list()

        # Initalise variable to store amount of fields for layout purposes (Could use length of list() but this is less confusing)
        self.number_of_fields = 0

        # Initalise grid layout of window.
        self.layout = QGridLayout()

        # Initalise the main widget of the window and set its layout to the main layout.
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        self.initalize_questions()
        self.initalize_buttons()
        
       
        
    def initalize_buttons(self):
        '''
            The function creates the 3 buttons required in the set questions window.
            It then assigned each of their functions and adds them to the layout.
        '''
        # Create AddButton and link to function add_question (through step_add)
        self.addButton = QPushButton("Add", self)
        self.addButton.setEnabled(True)
        self.addButton.clicked.connect(self.add_question)
        
        # Create removeButton and link to function remove_question 
        self.removeButton = QPushButton("Remove", self)
        self.removeButton.setEnabled(True)
        self.removeButton.clicked.connect(self.remove_question)
  
        # Create submitButton and link to function export_questions
        self.submitButton = QPushButton("Submit", self)
        self.submitButton.setEnabled(True)
        self.submitButton.clicked.connect(self.export_questions)
        
        # Add each button to the layout.
        self.layout.addWidget(self.addButton,0,0)
        self.layout.addWidget(self.removeButton,0,1)
        self.layout.addWidget(self.submitButton,0,2)
              
    def initalize_questions(self):
        '''
            This function parses over the current question list and adds fields/combo boxes to the window for each current question.
            Functionality for both sliders and binary questions is supported here.
        '''
        for q in self.questions:
            if q.get_type() == "rating scale":
                self.add_question(q.get_question(),0)
            elif q.get_type() == "Binary":
                self.add_question(q.get_question(),1)
            
    
    
    def add_question(self, text = None, type = 0):
        '''
            This is a function to add questions segments to the window. It will take a text input to assign the question, or set it to "Not set" if there is no input.
            If it is adding the first field, it will add a time_period box too.
        '''
        field = QLineEdit(self)
        if(not text):
            field.setText("Not set")
        else:
            field.setText(text)
        self.question_fields.append(field)
        self.number_of_fields = self.number_of_fields+1
        self.layout.addWidget(field,self.number_of_fields,0)
        
        # Adding of time period box. (This could be done somewhere else, this is kind of ugly.)
        if(self.number_of_fields == 1):
            time_label = QLabel("Time (in ms)")
            self.timeBox = QLineEdit(str(self.current_time))
            self.layout.addWidget(time_label, self.number_of_fields, 2)
            self.layout.addWidget(self.timeBox,self.number_of_fields+1,2)

            
        self.add_combo_box(type)
 
    def add_combo_box(self, type):
        '''
            This function is called inside add_question. It adds the combo box with the question types.
            Currently the Binary type is disabled because it has not been implemented into the player.
        '''
        comboBox = QComboBox(self)
        
        comboBox.addItem("rating scale")
        comboBox.addItem("binary")
        comboBox.model().item(1).setEnabled(False)
        comboBox.setCurrentIndex(type)

        self.layout.addWidget(comboBox, self.number_of_fields, 1)
        self.combo_box_list.append(comboBox)
        
    def remove_question(self):
        '''
            This function removes the latest label and combo box (segment) when called.
            This function cannot remove the first field, a design choice because that field stores the time_period variable.
        '''
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
    
    def export_questions(self):
        '''
            This function coverts the windows segments back into their logical equivalent in a questions list.
            It then sends this questions list back to the main window to be saved into the current program and stored on file.
        '''
        self.new_questions = list()
        for i in range(0, len(self.question_fields)):
            newQuestion = Question.Question()
            newQuestion.set_question(self.question_fields[i].text())
            newQuestion.set_type(self.combo_box_list[i].currentText())
            self.new_questions.append(newQuestion)
        

        self.parent.import_questions(self.new_questions, self.timeBox.text())
        self.close()

       
    