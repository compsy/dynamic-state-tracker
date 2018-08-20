
import gi
import json

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject


gi.require_version('GdkX11', '3.0')

import question
import statistics

# MATLAB dependancies
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import numpy as np
class ReviewWindow(Gtk.Window):#
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

        ##
        self.question_box = Gtk.Box()

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
        ##
        self.method_box = Gtk.Box()

        method_label = Gtk.Label("Select a method of review!")
        self.method_box.pack_start(method_label, False, False, 0)
        name_store = Gtk.ListStore(int, str)
        name_store.append([0, "Mean"])
        name_store.append([1, "Mode"])
        name_store.append([2, "Median"])
        name_store.append([3, "Range"])
        name_store.append([4, "Graph"])
        name_store.append([5, "Best fit(1D)"])
        name_store.append([6, "Best fit(2D)"])
        method_combo = Gtk.ComboBox.new_with_model_and_entry(name_store)
        method_combo.set_entry_text_column(1)
        method_combo.connect("changed", self.update_method)
        self.method_box.pack_start(method_combo, False, False, 0)



        self.main_box.add(self.method_box)


        ##
        self.value_box = Gtk.Box()
        self.value_string = Gtk.Label("None")

        self.value_box.pack_start(self.value_string, False, False, 0)
        self.main_box.add(self.value_box)

        ##

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
        self.update_value()
    def update_method(self, widget):
        self.active_method = widget.get_active()
        self.update_value()
    def update_value(self):
        self.value_string.set_text(str(self.calculate()))

    def calculate(self):
        temp_data = self.questions[self.active_question].get_data()
        if(self.active_method == 0):
            return sum(temp_data)/len(temp_data)
        if(self.active_method == 1):
            return max(set(temp_data), key=temp_data.count)
        if(self.active_method == 2):
            return statistics.median(temp_data)
        if(self.active_method == 3):
            return max(temp_data) - min(temp_data)
        if(self.active_method == 4):
            self.plot(temp_data)
        if(self.active_method == 5):
            self.best_fit(temp_data, 1)
        if(self.active_method == 6):
            self.best_fit(temp_data, 2)


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
        canvas.set_size_request(800, 600)
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

