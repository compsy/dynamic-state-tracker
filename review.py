
import gi
import json

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject


gi.require_version('GdkX11', '3.0')

import question
import statistics

# MATLAB dependancies
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
class ReviewWindow(Gtk.Window):
    def __init__(self, parent, save_directory):
        self.parent = parent
        Gtk.Window.__init__(self, title="Review")
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        last_part_of_path = save_directory.split("/")
        last_part_of_path = last_part_of_path[len(last_part_of_path) - 1].split(".")
        self.questions = list()
        self.active_question = 0
        self.active_method = 0

        self.title = Gtk.Label(last_part_of_path[0] + "\n\n\n")
        self.main_box.add(self.title)
        self.add(self.main_box)

        self.load_from_file(save_directory)

        ## SELECT QUESTION
        self.question_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        question_label = Gtk.Label("Select a question to review!")
        self.question_box.pack_start(question_label, False, False, 0)
        name_store = Gtk.ListStore(int, str)
        for i in range(0, len(self.questions)):
            name_store.append([1, self.questions[i].get_question()])

        
        question_combo = Gtk.ComboBox.new_with_model_and_entry(name_store)
        question_combo.set_entry_text_column(1)
        question_combo.connect("changed", self.update_question)
        self.question_box.pack_start(question_combo, False, False, 0)
        self.main_box.add(self.question_box)

	  
       ## ADD METHODs
				
        self.data_box = Gtk.Box()
        self.method_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
        method_mean = Gtk.Label("Mean: ")
        self.data_mean = Gtk.Label("0")
        box_mean = Gtk.Box()

        method_median = Gtk.Label("Median: ")
        self.data_median = Gtk.Label("0")
        box_median = Gtk.Box()
		
        method_mode = Gtk.Label("Mode: ")
        self.data_mode = Gtk.Label("0")
        box_mode = Gtk.Box()
		
        method_range = Gtk.Label("Range: ")
        self.data_range= Gtk.Label("0")
        box_range = Gtk.Box()
		
        box_mean.pack_start(method_mean, False, False, 0)
        box_mean.pack_start(self.data_mean, False, False, 0)
        box_median.pack_start(method_median, False, False, 0)
        box_median.pack_start(self.data_median, False, False, 0)
        box_mode.pack_start(method_mode, False, False, 0)
        box_mode.pack_start(self.data_mode, False, False, 0)
        box_range.pack_start(method_range, False, False, 0)
        box_range.pack_start(self.data_range, False, False, 0)
		
        self.method_box.add(box_mean)
        self.method_box.add(box_median)
        self.method_box.add(box_mode)
        self.method_box.add(box_range)
		
        self.data_box.add(self.method_box)
        
        self.main_box.add(self.data_box)
        self.update_values()
		
        
        ## Add 
        
        self.data_box.add(self.button_box)
        
        self.plot_button = Gtk.Button.new_with_label("Plot")
        self.plot_button.connect("clicked", self.plot_new)
        self.button_box.pack_end(self.plot_button, False, False, 0)
       
        self.plot_button = Gtk.Button.new_with_label("Plot with best fit")
        self.plot_button.connect("clicked", self.plot_best_new)
        self.button_box.pack_end(self.plot_button, False, False, 0)
       
        self.export_button = Gtk.Button.new_with_label("Export to excel")
        self.export_button.connect("clicked", self.write_to_excel)
        self.button_box.pack_end(self.export_button, False, False, 0)
        self.show_all()
        
        
       

    def load_from_file(self, dir):
        file = open(dir, "r")

        whole_file_string = file.read()
        segments = whole_file_string.split("//")

        self.video_dir = segments[0]
        self.time_interval = segments[1]
        for i in range(2, len(segments)-1):
            partition = segments[i].split(" - ")
            temp_data = json.loads(partition[1])
            temp_question = question.Question()
            temp_question.set_question(partition[0])
            temp_question.set_data(temp_data)
            self.questions.append(temp_question)



    def update_question(self, widget):
        self.active_question = widget.get_active()
        self.update_values()

    def update_values(self):
		temp_data = self.questions[self.active_question].get_data()
		self.data_mean.set_text(str(sum(temp_data)/len(temp_data)))
		self.data_median.set_text(str(statistics.median(temp_data)))
		self.data_mode.set_text(str(max(set(temp_data), key=temp_data.count)))
		self.data_range.set_text(str(max(temp_data) - min(temp_data)))
		
		
    def write_to_excel(self, widget):
		import xlwt
		
		workbook = xlwt.Workbook()
		worksheet = workbook.add_sheet("my sheet")
		
		yPos = 0
		xPos = 0
		for i in self.questions:
			worksheet.write(yPos, xPos, i.get_question())
			xPos = 1
			for n in i.get_data():
				worksheet.write(yPos, xPos, n)
				xPos = xPos+1
			yPos = yPos+1
		
		workbook.save("text.xls")
		
    def plot_new(self, widget):
		temp_data = self.questions[self.active_question].get_data()	
		pyplot.subplot(211)
		pyplot.plot(temp_data)	
		pyplot.title(self.questions[self.active_question].get_question())
		pyplot.show()
		
    def plot_best_new(self, widget):
        dimension = 2
		
        temp_data = self.questions[self.active_question].get_data()	
        pyplot.subplot(211)
        pyplot.plot(temp_data)	
		
		
        t = range(1, len(temp_data) + 1)
        fit = np.poly1d(np.polyfit(t, temp_data, dimension))
        format_fit = str(fit).replace('\n', '')
        
        pyplot.subplot(211)
        pyplot.plot(fit(t))
		
        pyplot.gcf().text(0.02, 0.25, format_fit, fontsize = 14)
        
        pyplot.title(self.questions[self.active_question].get_question())
        pyplot.show()
		
        
    def plot(self, temp_data):
        win = Gtk.Window()
        win.set_default_size(1000, 1000)
        win.set_title(self.questions[self.active_question].get_question())

        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        s = temp_data

        a.plot(s)
        a.set_xlabel("Time(x)")
        a.set_ylabel("Input(y)")
        sw = Gtk.ScrolledWindow()
        win.add(sw)
        # A scrolled window border goes outside the scrollbars and viewport
        sw.set_border_width(10)
        canvas = FigureCanvas(f)  # a Gtk.DrawingArea
        sw.add_with_viewport(canvas)

        win.show_all()

    def best_fit(self, temp_data, dimension):

        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        s = temp_data
        t = range(1, len(temp_data) + 1)
        fit = np.poly1d(np.polyfit(t, s, dimension))
        format_fit = str(fit).replace('\n', '')
        win = Gtk.Window()
        win.set_default_size(1000, 1000)
        title = self.questions[self.active_question].get_question() + "(y = %s)" % format_fit
        win.set_title(title)


        a.plot(s)
        a.plot(fit(t))
        a.set_xlabel("Time(x)")
        a.set_ylabel("Input(y)")
        sw = Gtk.ScrolledWindow()
        win.add(sw)
        # A scrolled window border goes outside the scrollbars and viewport
        sw.set_border_width(10)
        canvas = FigureCanvas(f)  # a Gtk.DrawingArea
        canvas.set_size_request(800, 600)
        sw.add_with_viewport(canvas)

        win.show_all()


