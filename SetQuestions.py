import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QButtonGroup)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QLineEdit, QGridLayout, QComboBox
import sys
import MediaPlayer
import Question
import MultiLanguage
class QuestionsWindow(QMainWindow):
    def __init__(self, parent=None, current_questions = None, current_time = None):
        super(QuestionsWindow, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle(self.parent.MultiLang.find_correct_word("Set items"))
        # Save parent for later use in saving questions
        
        
        # Store current questions from main program in local variable.
        self.questions = current_questions
        
        # Store current time period in local variable.
        self.current_time = current_time
        
        # Initalise widget lists for fields and combo boxes.
        self.question_fields = list()
        self.combo_box_list = list()
        self.question_max_fields = list()
        self.question_min_fields = list()
        
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
        self.initalize_labels()
       
        
    def initalize_buttons(self):
        '''
            The function creates the 3 buttons required in the set questions window.
            It then assigned each of their functions and adds them to the layout.
        '''
        # Create AddButton and link to function add_question (through step_add)
        self.addButton = QPushButton(self.parent.MultiLang.find_correct_word("Add"), self)
        self.addButton.setEnabled(True)
        self.addButton.clicked.connect(self.add_question)
        
        # Create removeButton and link to function remove_question 
        self.removeButton = QPushButton(self.parent.MultiLang.find_correct_word("Remove"), self)
        self.removeButton.setEnabled(True)
        self.removeButton.clicked.connect(self.remove_question)
  
        # Create submitButton and link to function export_questions
        self.submitButton = QPushButton(self.parent.MultiLang.find_correct_word("Submit"), self)
        self.submitButton.setEnabled(True)
        self.submitButton.clicked.connect(self.export_questions)
        
        # Add each button to the layout.
        self.layout.addWidget(self.addButton,0,0)
        self.layout.addWidget(self.removeButton,0,1)
        self.layout.addWidget(self.submitButton,0,2)
        
        
 
    def initalize_labels(self):

        # Adding of time period box.
        time_label = QLabel(self.parent.MultiLang.find_correct_word("Time") + " (in ms):")
        self.timeBox = QLineEdit(str(self.current_time))
        self.layout.addWidget(time_label, 0, 3)
        self.layout.addWidget(self.timeBox,0,4)

        
        question_name = QLabel(self.parent.MultiLang.find_correct_word("Questions"))
        self.layout.addWidget(question_name, 1, 0)
        
        question_min =QLabel(self.parent.MultiLang.find_correct_word("Minimum"))
        self.layout.addWidget(question_min, 1, 1)
        
        question_max = QLabel(self.parent.MultiLang.find_correct_word("Maximum"))
        self.layout.addWidget(question_max, 1, 2)
              
    def initalize_questions(self):
        '''
            This function parses over the current question list and adds fields/combo boxes to the window for each current question.
            Functionality for both sliders and binary questions is supported here.
        '''
        for q in self.questions:
            if q.get_type() == "continuous":
                self.add_question(q.get_question(), q.get_min(), q.get_max() ,0)
            elif q.get_type() == "Binary":
                self.add_question(q.get_question(), q.get_min(), q.get_max() ,1)
            
    
    
    def add_question(self, text = None, min = None, max = None, type = 0):
        '''
            This is a function to add questions segments to the window. It will take a text input to assign the question, or set it to "Not set" if there is no input.
            If it is adding the first field, it will add a time_period box too.
        '''
        if(self.number_of_fields == 7):
            print("7 is max number of questions!")
            return
        
        field = QLineEdit(self)
        if(not text):
            field.setText("Not set")
        else:
            field.setText(text)
        self.question_fields.append(field)
        self.number_of_fields = self.number_of_fields+1
        self.layout.addWidget(field,self.number_of_fields+1,0)
        
        max_field = QLineEdit(self.parent.MultiLang.find_correct_word("Very much"))
        min_field = QLineEdit(self.parent.MultiLang.find_correct_word("Not at all"))
        if( min ):
            min_field.setText(min)
        if( max ):
            max_field.setText(max)

            
        self.layout.addWidget(min_field,self.number_of_fields+1,1)
        self.layout.addWidget(max_field,self.number_of_fields+1,2)
        self.question_max_fields.append(max_field)
        self.question_min_fields.append(min_field)

            
        self.add_combo_box(type)
 
    def add_combo_box(self, type):
        '''
            This function is called inside add_question. It adds the combo box with the question types.
            Currently the Binary type is disabled because it has not been implemented into the player.
        '''
        comboBox = QComboBox(self)
        
        comboBox.addItem(self.parent.MultiLang.find_correct_word("continuous"))
        comboBox.addItem("binary")
        comboBox.model().item(1).setEnabled(False)
        comboBox.setCurrentIndex(type)

        self.layout.addWidget(comboBox, self.number_of_fields+1, 3)
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
        
        max_field_to_remove = self.question_max_fields.pop()
        max_field_to_remove.deleteLater()
        self.layout.removeWidget(max_field_to_remove)
        
        min_field_to_remove = self.question_min_fields.pop()
        min_field_to_remove.deleteLater()
        self.layout.removeWidget(min_field_to_remove)
        
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
            newQuestion.set_min_max(self.question_min_fields[i].text(), self.question_max_fields[i].text())
            string_type = self.combo_box_list[i].currentText()
            if(string_type == self.parent.MultiLang.find_correct_word("continuous") ):
                 newQuestion.set_type("continuous")

            self.new_questions.append(newQuestion)
        

        self.parent.import_questions(self.new_questions, self.timeBox.text())
        self.close()

       
    