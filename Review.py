import PyQt5 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QComboBox, QGridLayout, QLineEdit, QHBoxLayout, QCheckBox
from PyQt5.QtGui import QIcon,QFont
import sys
import json
import Question
import Form
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import statistics
import MultiLanguage

class ReviewWindow(QMainWindow):
    def __init__(self, parent=None, file_name=None):
        super(ReviewWindow, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Dynamic State Tracker 2.0: " +self.parent.MultiLang.find_correct_word("Review"))
        self.questions = list()
        self.form_list = list()
        self.load_file(file_name)
        
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        # Create DST title label
        titleLabel = QLabel("DST 2.0 : " +self.parent.MultiLang.find_correct_word("Show result"), self)
        self.layout.addWidget(titleLabel, 0, 1)

        # Initalize plot.
        self.plot = PlotCanvas(self, 5, 4, 100)
        
        # Add both combo boxes to the window.
        self.add_combo_boxes()
        # Set default question to 0 (For graphing purposes).
        self.question_index = 0
        # Initialise the fit, setting its default value to "None"
        self.fit = "None"
        
        # Add the plot to the window.
        self.add_other_buttons()
        self.add_plot_with_best_fit()
        
        
        # Add actions 
        openAction = QAction(QIcon('open.png'), '&OpenMore', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open more')
        openAction.triggered.connect(self.load_more_data)
        
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        
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
            
    def load_more_data(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "saves","All Files (*);;Python Files (*.py)")
        
        if fileName:
            #print(fileName)
            f = open(fileName, 'r')
            with f:
                data = f.read()
                
            split_between_question_and_form_data = data.split("~")
        
            question_segments = split_between_question_and_form_data[0].split("//")
            form_segments =  split_between_question_and_form_data[1].split("//")
            
            print("Base time: " + self.time_interval + ". New time: " + question_segments[1])
            if(self.time_interval != question_segments[1]):
                print("Different time-intervals. Failed to merge!")
                return
            for i in range(2, len(question_segments)-1):
                partition = question_segments[i].split(" - ")
                temp_data = json.loads(partition[1])
                if(len(self.questions) > 0 and len(temp_data) != len(self.questions[0].get_data())):
                    print("Warning: Different lengths of input. Base length = " + str(len(self.questions[0].get_data())) + " and new length = " + str( len(temp_data)))
                    
                temp_question = Question.Question()
                temp_question.set_question(partition[0])
                temp_question.set_data(temp_data)
                self.questions.append(temp_question)
                
                # Add to the combo box!
                self.comboBox.addItem(partition[0])
                
                if(len(self.questions) > 1):
                    self.plot_all.setEnabled(True)
 
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
        self.comboBoxDim.addItem(self.parent.MultiLang.find_correct_word("No trend"))
        self.comboBoxDim.addItem(self.parent.MultiLang.find_correct_word("Trend") + " (x)")
        self.comboBoxDim.addItem(self.parent.MultiLang.find_correct_word("Trend") +f' (x\N{SUPERSCRIPT TWO})') 
        self.comboBoxDim.addItem(self.parent.MultiLang.find_correct_word("Trend") +f' (x\N{SUPERSCRIPT THREE})') 
        self.comboBoxDim.addItem(self.parent.MultiLang.find_correct_word("Trend") +f' (x\N{SUPERSCRIPT FOUR})')     

        
         
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
        self.replot()
         
    def set_dimension(self):
        '''
            Clear the current plot and reload with new best fit.
        ''' 
        self.replot()
         
        
    def add_plot_with_best_fit(self):
        '''
            Creates a graph, adds it too the window. Also graphs the data from the first question at the default degree.
        '''
        self.fit = self.plot.best_fit(self.comboBoxDim.currentIndex())
        self.layout.addWidget(self.plot, 3, 1)
    
    def add_other_buttons(self):
        '''
            Add the export and statistics buttons and assigns their click function.
        '''
        export_button = QPushButton(self.parent.MultiLang.find_correct_word("Export"))
        export_button.clicked.connect(self.write_to_excel)
        self.layout.addWidget(export_button, 4, 1)
        
        stats_button = QPushButton(self.parent.MultiLang.find_correct_word("Statistics"))
        stats_button.clicked.connect(self.open_stats_window)
        self.layout.addWidget(stats_button, 5, 1)
        
        
        checkButtonLayout = QHBoxLayout()
        checkButtonLayout.setContentsMargins(0, 0, 0, 0)

        self.layout.addLayout(checkButtonLayout, 6, 1)
        
        #self.hide_best_fit = QCheckBox(self.parent.MultiLang.find_correct_word("No trend"))
        #self.hide_best_fit.stateChanged.connect(self.replot)
        #checkButtonLayout.addWidget(self.hide_best_fit)
        
        self.add_grid = QCheckBox(self.parent.MultiLang.find_correct_word("Grid"))
        self.add_grid.stateChanged.connect(self.replot)
        checkButtonLayout.addWidget(self.add_grid)
        
        self.set_to_normal = QPushButton("Normal plot")
        self.set_to_normal.clicked.connect(self.replot)
        checkButtonLayout.addWidget(self.set_to_normal)
          
        self.set_to_histo = QPushButton("Histogram")
        self.set_to_histo.clicked.connect(self.plot.histogram)
        checkButtonLayout.addWidget(self.set_to_histo)
        
        
        self.plot_all = QPushButton("Plot all")
        self.plot_all.clicked.connect(self.plot.plot_all)
        checkButtonLayout.addWidget(self.plot_all)
        if(len(self.questions) == 1):
            self.plot_all.setEnabled(False)
        
        self.more_options = QPushButton("More/Less options")
        self.more_options.clicked.connect(self.toggle_more_buttons)
        checkButtonLayout.addWidget(self.more_options)
              
              
              
        moreButtonLayout = QHBoxLayout()
        moreButtonLayout.setContentsMargins(0, 0, 0, 0)

        self.layout.addLayout(moreButtonLayout, 7, 1)
        
        
        self.set_to_diff_histo = QPushButton("dx Histogram")
        self.set_to_diff_histo.clicked.connect(self.plot.forwards_difference_histogram)
        moreButtonLayout.addWidget(self.set_to_diff_histo)
        self.set_to_diff_histo.setHidden(True)
        
        
        self.fourier_button = QPushButton("Fourier")
        self.fourier_button.clicked.connect(self.plot.fourier_transform)
        moreButtonLayout.addWidget(self.fourier_button)
        self.fourier_button.setHidden(True)
    
        self.state_space = QPushButton("State space")
        self.state_space.clicked.connect(self.open_state_space)
        moreButtonLayout.addWidget(self.state_space)  
        self.state_space.setHidden(True)


    def toggle_more_buttons(self):
        self.set_to_diff_histo.setHidden(not self.set_to_diff_histo.isHidden())
        self.fourier_button.setHidden(not self.fourier_button.isHidden())
        self.state_space.setHidden(not self.state_space.isHidden())
        
    def open_state_space(self):
        new_window = StateSpaceWindow(self)
        
    def open_stats_window(self):
        new_window = StatsWindow(self, self.fit)
        new_window.show()
        
    def write_to_excel(self, widget):
       window = SaveExcel(self)
        
    def replot(self):
        self.fit = self.plot.best_fit(self.comboBoxDim.currentIndex())
        
        
class StatsWindow(QMainWindow):
    def __init__(self, parent=None, best_fit = None):
        super(StatsWindow, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle(self.parent.parent.MultiLang.find_correct_word("Statistics"))

        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)

        # Create average labels.
        self.data_mean = QLabel("0")
        self.data_median = QLabel("0")
        self.data_mode = QLabel("0")
        self.data_range= QLabel("0")
        self.data_standard_dev = QLabel("0")
        
        # Creates the best fit label, sets its text to the formated best fit.
        self.best_fit = QLabel(self.parent.parent.MultiLang.find_correct_word("Trend") + ": " + self.format_best_fit(best_fit))
        
        # Set all widgets to the layout.
        self.layout.addWidget(self.data_mean, 0,0)
        self.layout.addWidget(self.data_median, 1,0)        
        self.layout.addWidget(self.data_mode, 2,0)
        self.layout.addWidget(self.data_range, 3,0)      
        self.layout.addWidget(self.best_fit, 4,0)
        self.layout.addWidget(self.data_standard_dev, 5, 0)

        # Update values of the averages to the set question.
        self.update_values()
      
        
    def update_values(self):
        '''
            Updates all the averages, based off the selected question.
            This is really only used as an initalization function (Because it looks neater).
        '''
        temp_data = self.parent.questions[self.parent.question_index].get_data()
        self.data_mean.setText(self.parent.parent.MultiLang.find_correct_word("Mean") + ": " + str(round(sum(temp_data)/len(temp_data), 3)))
        self.data_median.setText(self.parent.parent.MultiLang.find_correct_word("Median") + ": " + str(statistics.median(temp_data)))
        self.data_mode.setText(self.parent.parent.MultiLang.find_correct_word("Mode") + ": " + str(max(set(temp_data), key=temp_data.count)))
        self.data_range.setText(self.parent.parent.MultiLang.find_correct_word("Range")+ ": " + str(max(temp_data) - min(temp_data)))
        self.data_standard_dev.setText("Standard deviation: " + str(round(np.std(temp_data), 3)))
        
    def format_best_fit(self, fit):
        '''
            This formats the fit array into a nice string.
            Uses the i as a counter for the degree of x. Counting backwards from the length of the data.
            If the number is negative, add it as it, else add a +.
        '''
        i = len(fit)
        return_string = ""
        for part in fit:
            # Is the first char is N, it must be "None" so return "None"
            if( str(part) == "N"):
                return "None"
                
            formatedNumber = round(float(part), 3)
            if(i == 0):
                xString = ""
            elif(i == 1):
                xString = f' x'
            elif(i == 2):
                xString = f' x\N{SUPERSCRIPT TWO}'
            elif(i == 3):
                xString = f' x\N{SUPERSCRIPT THREE}'
            elif(i == 4):
                xString = f' x\N{SUPERSCRIPT FOUR}'

            
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
            If the degree is 0, no trend line will be created. The 'fit' variable will remain as default "None".
            If the plot excepts, then it is most likely the wrong text file was loaded. This prints "Plot crashing!" and closes the review window.
        '''
        self.clear()
        try:
            data = self.parent.questions[self.parent.question_index].get_data()
            ax = self.figure.add_subplot(111)
            time_str = self.parent.parent.MultiLang.find_correct_word("Time")
            ax.set(xlabel = time_str + " (" + self.parent.time_interval + " ms)", ylabel = self.parent.parent.MultiLang.find_correct_word("Not at all to very much"))
            ax.plot(data, 'r-')
            ax.set_title(self.parent.questions[self.parent.question_index].get_question())
            
            # Initalize fit, incase dimension = 0
            fit = 'None'
            
            # Create time series (for x values)
            t = range(1, len(data) + 1)
             
            # Create best fit, depending on dimension.
            if(dimension != 0):
                
                fit = np.poly1d(np.polyfit(t, data, dimension))
                ax.plot(fit(t))
            
            if(self.parent.add_grid.isChecked()):
                ax.grid()
                
            # Draw graph.    
            self.draw()
            return fit
        except:
            print("Plot crashing!")
            self.parent.close()
            self.close()
            
    def histogram(self):
        self.clear()
        try:
            data = self.parent.questions[self.parent.question_index].get_data()
            ax = self.figure.add_subplot(111)
            ax.hist(data, bins = 10)
            ax.set(xlabel = "User input by 10's", ylabel = "Amount")
            tick_val = [0,10,20,30,40,50,60,70,80,90,100]
            ax.set_xticks(tick_val)
            ax.set_title("Histogram:" + self.parent.questions[self.parent.question_index].get_question())
            
            if(self.parent.add_grid.isChecked()):
                ax.grid()
            self.draw()
            return None
        except:
            print("Histo crashing!")
            self.parent.close()
            self.close()
            
            
    def plot_all(self):
        self.clear()
        colors = ["red", "blue", "green", "black", "purple", "yellow", "pink"]
        legend_list = list()
        i = 0
        for question in self.parent.questions:
            ax = self.figure.add_subplot(111)
            ax.plot(question.get_data(), c = colors[i])
            legend_list.append(mpatches.Patch(color = colors[i], label=question.get_question()))
            i = i +1
        
        if(self.parent.add_grid.isChecked()):
                ax.grid()
        ax.set_title("All questions")
        time_str = self.parent.parent.MultiLang.find_correct_word("Time")
        ax.set(xlabel = time_str + " (" + self.parent.time_interval + " ms)", ylabel = self.parent.parent.MultiLang.find_correct_word("Not at all to very much"))
        
        # Add legend
        ax.legend(handles = legend_list)
        #Draw graphs 
        self.draw()
        
    def fourier_transform(self):
         self.clear()
         data = self.parent.questions[self.parent.question_index].get_data()
         transform = np.fft.fft(data)
         #print(transform)
         if(self.parent.add_grid.isChecked()):
            ax.grid()
         ax = self.figure.add_subplot(111)
         ax.set(xlabel = "Freqency (Hz)", ylabel = "Amount")
         ax.plot(transform)
         self.draw()
         
    def forwards_difference_histogram(self): ## Basically calculating absolute descrete velocity and putting it into bins.
        self.clear()
        data = self.parent.questions[self.parent.question_index].get_data()
        difference_list = list()
        for i in range (0, len(data)-1):
            difference_list.append(abs(data[i] - data[i+1]))
            
        ax = self.figure.add_subplot(111)
        ax.hist(difference_list, bins = 10)
        ax.set(xlabel = "Forward difference", ylabel = "Amount")
        #tick_val = [0,10,20,30,40,50,60,70,80,90,100]
        #ax.set_xticks(tick_val)
        ax.set_title("Histogram:" + self.parent.questions[self.parent.question_index].get_question())
        
        if(self.parent.add_grid.isChecked()):
            ax.grid()
        self.draw()
    def clear(self):
        '''
           This clears the plot from the figure.
           Maybe I should just have this used in best_fit? 
        '''
        self.axes.clear()
        
        
        
class SaveExcel(QMainWindow):
     def __init__(self, parent=None):
        super(SaveExcel, self).__init__(parent)
        self.setWindowTitle("Export file as:")
        self.parent = parent
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        self.file_name_box = QLineEdit("File name here")
        self.layout.addWidget(self.file_name_box, 0, 0)
        
        self.save_button = QPushButton(self.parent.parent.MultiLang.find_correct_word("Save") +  " file")
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
        
        # Add in time stamps for data
        if(not len(self.parent.questions) == 0):
            worksheet.write(0, xPos, self.parent.parent.MultiLang.find_correct_word("Time") + "(in ms)")
            time_index = 1
            for n in self.parent.questions[0].get_data():
                worksheet.write(time_index, xPos, str(int(time_index)*int(self.parent.time_interval)))
                time_index = time_index+1
                
                
        # Add in data        
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
        
class StateSpaceWindow(QMainWindow):
     def __init__(self, parent=None):
        super(StateSpaceWindow, self).__init__(parent)
        self.setWindowTitle("Chose data to create state space")
        self.parent = parent
        self.questions = parent.questions
        self.layout = QGridLayout()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget) 
        self.main_widget.setLayout(self.layout)
        
        # Create options
        
           
        checkButtonLayout = QHBoxLayout()
        checkButtonLayout.setContentsMargins(0, 0, 0, 0)
        
        self.use_best_fit = QCheckBox("Use best fit")
        checkButtonLayout.addWidget(self.use_best_fit)
        
        self.dim_tag = QLabel("Dimension:")
        self.dim = QLineEdit("3")
        checkButtonLayout.addWidget(self.dim_tag)
        checkButtonLayout.addWidget(self.dim)
         
            
        self.iter_tag = QLabel("Iter:")
        self.iter = QLineEdit("100")
        checkButtonLayout.addWidget(self.iter_tag)
        checkButtonLayout.addWidget(self.iter)
        
        self.layout.addLayout(checkButtonLayout, 0, 1)
        
        # Create question box and add each loaded question into it.
        self.comboBox1 = QComboBox(self)
        for q in self.questions:
            self.comboBox1.addItem(q.get_question())

        self.layout.addWidget(self.comboBox1, 1, 1)
        
        
        # Create question box and add each loaded question into it.
        self.comboBox2 = QComboBox(self)
        for q in self.questions:
            self.comboBox2.addItem(q.get_question())

        self.layout.addWidget(self.comboBox2, 2, 1)
        
        # Create question box and add each loaded question into it.
        self.comboBox3 = QComboBox(self)
        for q in self.questions:
            self.comboBox3.addItem(q.get_question())

        self.layout.addWidget(self.comboBox3, 3, 1)
        
        
        self.submit = QPushButton(self.parent.parent.MultiLang.find_correct_word("Submit"))
        self.submit.clicked.connect(self.plot_state_space)
        self.layout.addWidget(self.submit, 4, 1)
        
        self.show()
        
     def plot_state_space(self):
        import matplotlib as mpl
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        a = self.parent.questions[self.comboBox1.currentIndex()].get_data()
        b = self.parent.questions[self.comboBox2.currentIndex()].get_data()
        c = self.parent.questions[self.comboBox3.currentIndex()].get_data()
        
        ax.set(xlabel = self.parent.questions[self.comboBox1.currentIndex()].get_question(), ylabel = self.parent.questions[self.comboBox2.currentIndex()].get_question(), zlabel = self.parent.questions[self.comboBox3.currentIndex()].get_question())
        
     
        
        
        if (self.use_best_fit.isChecked()):
            a = np.poly1d(np.polyfit(range(0, len(a)), a, int(self.dim.text())))
            b = np.poly1d(np.polyfit(range(0, len(b)), b, int(self.dim.text())))
            c = np.poly1d(np.polyfit(range(0, len(c)), c, int(self.dim.text())))
            
            iter = int(self.iter.text())
            
          
            
            new_a = list()
            new_b = list()
            new_c = list()
            
            for i in range(0, iter):
                new_a.append(a(i))
                new_b.append(b(i))
                new_c.append(c(i))
            
            a = new_a
            b = new_b
            c = new_c
            
            print(a)
        else:
            # Ensure all datasets are the same length!
            minimum = min(len(a), len(b), len(c))
            a = a[:minimum]
            b = b[:minimum]
            c = c[:minimum]
        
        ax.plot(a, b, c)
        
        ax.legend()

        plt.show()
     