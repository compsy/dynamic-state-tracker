import PyQt5
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QButtonGroup)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QLineEdit, QGridLayout, QComboBox
import sys
import MediaPlayer
import Form
import MultiLanguage
class SetFormWindow(QMainWindow):
    def __init__(self, parent=None, form_list = None):
        super(SetFormWindow, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle(self.parent.MultiLang.find_correct_word("Set Form"))
        
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
  
        # Create submitButton and link to function export_form
        self.submitButton = QPushButton(self.parent.MultiLang.find_correct_word("Submit"), self)
        self.submitButton.setEnabled(True)
        self.submitButton.clicked.connect(self.export_form)
        
        # Add each button to the layout.
        self.layout.addWidget(self.addButton,0,0)
        self.layout.addWidget(self.removeButton,1,0)
        self.layout.addWidget(self.submitButton,2,0)

        
    def initalize_questions(self):
        '''
            This function parses over the current question list and adds fields to the window for each current question.
        '''
        for q in self.form_list:
            self.add_question(q.get_question(),1)
            
    
    
    def add_question(self, text = None, type = 0):
        '''
            This is a function to add questions segments to the window. 
            It will take a text input to assign the question, or set it to "Not set" if there is no input.
        '''
        field = QLineEdit(self)
        if(not text):
            field.setText("Not set")
        else:
            field.setText(text)
        self.question_fields.append(field)
        self.number_of_fields = self.number_of_fields+1
        self.layout.addWidget(field,3+self.number_of_fields,0)
      
        

    def remove_question(self):
        '''
            This function removes the latest label (segment) when called.
            You cannot remove a question when you have no questions.
        '''
        if(self.number_of_fields == 0):
            print("You already have 0 questions")
            return
        field_to_remove = self.question_fields.pop()
        field_to_remove.deleteLater()
        self.layout.removeWidget(field_to_remove)
        self.number_of_fields = self.number_of_fields-1

    
    def export_form(self):
        '''
            This function coverts the windows segments back into their logical equivalent in a form list.
            It then sends this form list back to the main window to be saved into the current program and stored on file.
        '''
        self.new_form_list = list()
        for i in range(0, len(self.question_fields)):
            newFormComponent = Form.Form()
            newFormComponent.set_question(self.question_fields[i].text())
            self.new_form_list.append(newFormComponent)
        

        self.parent.import_form(self.new_form_list)
        self.close()

       
    