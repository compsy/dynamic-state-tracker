import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QComboBox, QGridLayout
import sys
import json
import Question

 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ReviewWindow(QMainWindow):
    def __init__(self, parent=None, file_name=None):
        super(ReviewWindow, self).__init__(parent)
        
        self.questions = list()
        self.load_file(file_name)
        
        
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)

        
        
        # Create DST title label
        titleLabel = QLabel("DST 2.0 : Review", self)
        self.layout.addWidget(titleLabel, 0, 1)
        
        
        
        
        self.add_combo_box()
        self.question_index = 0
        
        self.add_plot()
        
    def load_file(self, file_name):
        f = open(file_name, 'r')
        with f:
            data = f.read()
            self.load_data(data)

    def load_data(self, data):  
        segments = data.split("//")

        self.video_dir = segments[0]
        self.time_interval = segments[1]
        for i in range(2, len(segments)-1):
           
            partition = segments[i].split(" - ")
            temp_data = json.loads(partition[1])
            temp_question = Question.Question()
            temp_question.set_question(partition[0])
            temp_question.set_data(temp_data)
            self.questions.append(temp_question)
        print("Load complete!")
        
    
    def add_combo_box(self):
        self.comboBox = QComboBox(self)
        
        for q in self.questions:
            self.comboBox.addItem(q.get_question())

        self.comboBox.activated[str].connect(self.set_question)
        
        self.layout.addWidget(self.comboBox, 1, 1)
    
    def set_question(self, text):
         self.question_index = self.comboBox.currentIndex()
         
         self.plot.clear()
         self.plot.plot()
         
         
         
    def add_plot(self):
        self.plot = PlotCanvas(self, 5, 4, 100)
        
        self.layout.addWidget(self.plot, 2, 1)
    
 
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.parent = parent
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
 
 
    def plot(self):
        data = self.parent.questions[self.parent.question_index].get_data()
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title(self.parent.questions[self.parent.question_index].get_question())
        self.draw()
        
    def clear(self):
        self.axes.clear()