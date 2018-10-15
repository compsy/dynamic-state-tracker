import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QComboBox, QGridLayout, QLineEdit
import sys
import json
import Question
import Form
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import statistics

class ReviewWindow(QMainWindow):
    def __init__(self, parent=None, file_name=None):
        super(ReviewWindow, self).__init__(parent)
        
        self.questions = list()
        self.form_list = list()
        self.load_file(file_name)
        
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        # Create DST title label
        titleLabel = QLabel("DST 2.0 : Review", self)
        self.layout.addWidget(titleLabel, 0, 1)

        # Add both combo boxes to the window.
        self.add_combo_boxes()
        # Set default question to 0 (For graphing purposes).
        self.question_index = 0
        # Initialise the fit, setting its default value to "None"
        self.fit = "None"
        
        # Add the plot to the window.
        self.add_plot_with_best_fit()
        self.add_other_buttons()
        
    def load_file(self, file_name):
        '''
            Opens a file, then uses load_data on the read text to load questions and data into the reviewing format.
        '''
        f = open(file_name, 'r')
        with f:
            data = f.read()
            self.load_data(data)

    def load_data(self, data):
        '''
            The inital split should be into two strings. The first is the questions, with their respective answers.
            The second is the form questions with the form data. The questions set of data is used in the reviewing.
            The form set of data is exported with the question data, but not used in the program (currently).
            The first two parts of the 'question data' are meta data, they contain the 'video url' and used 'time-interval' respectively. 
        '''
        split_between_question_and_form_data = data.split("~")
        
        question_segments = split_between_question_and_form_data[0].split("//")
        form_segments =  split_between_question_and_form_data[1].split("//")
        
        self.video_dir = question_segments[0]
        self.time_interval = question_segments[1]
        for i in range(2, len(question_segments)-1):
            partition = question_segments[i].split(" - ")
            temp_data = json.loads(partition[1])
            temp_question = Question.Question()
            temp_question.set_question(partition[0])
            temp_question.set_data(temp_data)
            self.questions.append(temp_question)
            
        for i in range(0, len(form_segments)-1):
            partition = form_segments[i].split(" - ")
            temp_form = Form.Form()
            temp_form.set_question(partition[0])
            temp_form.set_data(partition[1])
            self.form_list.append(temp_form)
 
    def add_combo_boxes(self):
        '''
            Add two combo boxes, one for each question, and one for the polynomial representation used.
        '''
        # Create question box and add each loaded question into it.
        self.comboBox = QComboBox(self)
        for q in self.questions:
            self.comboBox.addItem(q.get_question())

        self.comboBox.activated.connect(self.set_question)
        self.layout.addWidget(self.comboBox, 1, 1)
        
        # 0-4 degrees in the polynomial best fit. 
        self.comboBoxDim = QComboBox(self)
        self.comboBoxDim.addItem("0")
        self.comboBoxDim.addItem("1")
        self.comboBoxDim.addItem("2") 
        self.comboBoxDim.addItem("3") 
        self.comboBoxDim.addItem("4")     

        # Set default to 3. A cubic.
        self.comboBoxDim.setCurrentIndex(3)
        self.comboBoxDim.activated.connect(self.set_dimension)
        self.layout.addWidget(self.comboBoxDim, 2, 1)
        
    def set_question(self):
        '''
            When the question box is changed, it sets the question_index, so when the graphing function loads the question data it has the correct question.
            This is a bit archaic, I should check the index of the combo box when I load the data instead (maybe in the future!)
        '''
        self.question_index = self.comboBox.currentIndex()
        
        # Clear the current plot and regraph with regard to the new data from the new question.
        self.plot.clear()
        self.fit = self.plot.best_fit(self.comboBoxDim.currentIndex())
         
    def set_dimension(self):
        '''
            Clear the current plot and reload with new best fit.
        ''' 
        self.plot.clear()
        self.fit = self.plot.best_fit(self.comboBoxDim.currentIndex())
         
        
    def add_plot_with_best_fit(self):
        '''
            Creates a graph, adds it too the window. Also graphs the data from the first question at the default degree.
        '''
        self.plot = PlotCanvas(self, 5, 4, 100)
        self.fit = self.plot.best_fit(self.comboBoxDim.currentIndex())
        self.layout.addWidget(self.plot, 3, 1)
    
    def add_other_buttons(self):
        '''
            Add the export and statistics buttons and assigns their click function.
        '''
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.write_to_excel)
        self.layout.addWidget(export_button, 4, 1)
        
        stats_button = QPushButton("Statistics")
        stats_button.clicked.connect(self.open_stats_window)
        self.layout.addWidget(stats_button, 5, 1)

    def open_stats_window(self):
        new_window = StatsWindow(self, self.fit)
        new_window.show()
        
    def write_to_excel(self, widget):
       window = SaveExcel(self)
        
class StatsWindow(QMainWindow):
    def __init__(self, parent=None, best_fit = None):
        super(StatsWindow, self).__init__(parent)
        self.parent = parent
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)

        # Create average labels.
        self.data_mean = QLabel("0")
        self.data_median = QLabel("0")
        self.data_mode = QLabel("0")
        self.data_range= QLabel("0")
        
        # Creates the best fit label, sets its text to the formated best fit.
        self.best_fit = QLabel("best fit: " + self.format_best_fit(best_fit))

        # Set all widgets to the layout.
        self.layout.addWidget(self.data_mean, 0,0)
        self.layout.addWidget(self.data_median, 1,0)        
        self.layout.addWidget(self.data_mode, 2,0)
        self.layout.addWidget(self.data_range, 3,0)      
        self.layout.addWidget(self.best_fit, 4,0)

        # Update values of the averages to the set question.
        self.update_values()
      
        
    def update_values(self):
        '''
            Updates all the averages, based off the selected question.
            This is really only used as an initalization function (Because it looks neater).
        '''
        temp_data = self.parent.questions[self.parent.question_index].get_data()
        self.data_mean.setText("Mean: " + str(sum(temp_data)/len(temp_data)))
        self.data_median.setText("Median: " + str(statistics.median(temp_data)))
        self.data_mode.setText("Mode: " + str(max(set(temp_data), key=temp_data.count)))
        self.data_range.setText("Range: " + str(max(temp_data) - min(temp_data)))
        
    def format_best_fit(self, fit):
        '''
            This formats the fit array into a nice string.
            Uses the i as a counter for the degree of x. Counting backwards from the length of the data.
            If the number is negative, add it as it, else add a +.
        '''
        i = len(fit)
        return_string = ""
        for part in fit:
            print("part: " + str(part))
            # Is the first char is N, it must be "None" so return "None"
            if( str(part) == "N"):
                return "None"
                
            # Ugly rounding to 3dp.
            formatedNumber = int(1000*float(part))/1000
            
            if(i == 0):
                xString = ""
            else:
                xString = "x^(" + str(i) + ")"
            
            if(return_string == ""):
                 return_string += str(formatedNumber) + xString
            else:
                if(formatedNumber < 0):
                    return_string += " " + str(formatedNumber) + xString 
                else:
                    return_string += " + " + str(formatedNumber) + xString 
            i = i-1
        return return_string
            
                  
 
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

    def best_fit(self, dimension):
        '''
            Sets the figure in PlotCanvas. Creates a graph using the question selected and the degree selected.
            If the degree is 0, no best fit line will be created. The 'fit' variable will remain as default "None".
            If the plot excepts, then it is most likely the wrong text file was loaded. This prints "Plot crashing!" and closes the review window.
        '''
        try:
            data = self.parent.questions[self.parent.question_index].get_data()
            ax = self.figure.add_subplot(111)
            ax.plot(data, 'r-')
            ax.set_title(self.parent.questions[self.parent.question_index].get_question() + ". Time (" + self.parent.time_interval + " ms)")
            fit = 'None'
            if(dimension != 0):
                t = range(1, len(data) + 1)
                fit = np.poly1d(np.polyfit(t, data, dimension))
                ax.plot(fit(t))
            self.draw()
            return fit
        except:
            print("Plot crashing!")
            self.parent.close()
            self.close()
   
    def clear(self):
        '''
           This clears the plot from the figure.
           Maybe I should just have this used in best_fit? 
        '''
        self.axes.clear()
        
        
        
class SaveExcel(QMainWindow):
     def __init__(self, parent=None):
        super(SaveExcel, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        self.file_name_box = QLineEdit("File name here")
        self.layout.addWidget(self.file_name_box, 0, 0)
        
        self.save_button = QPushButton("Save file")
        self.save_button.clicked.connect(self.save)
        self.layout.addWidget(self.save_button, 0, 1)
        
        self.show()
        
     def save(self):
        '''
            Here we use xlwt to output to a xls file. We output both the form data and the question data. The output is seperated by a gap in the column.
        '''
        import xlwt
		
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet("my sheet")
		
        xPos = 0        
        for i in self.parent.form_list:
            worksheet.write(0, xPos, i.get_question())
            worksheet.write(1, xPos, i.get_data())
            xPos = xPos+1
        
        xPos = xPos+1   
        for i in self.parent.questions:
            yPos = 0
            worksheet.write(yPos, xPos, i.get_question())
            yPos = 1
            for n in i.get_data():
                worksheet.write(yPos, xPos, n)
                yPos = yPos+1
            xPos = xPos+1
		
        workbook.save("exports/" + self.file_name_box.text() + ".xls")
        self.close()