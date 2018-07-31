
import gi


gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject


gi.require_version('GdkX11', '3.0')

import question
class SettingsWindow(Gtk.Window):#


    def __init__(self, parent, cur_questions, cur_time):
        self.cur_questions = cur_questions
        self.parent = parent
        Gtk.Window.__init__(self, title="Options")
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_box)
        self.button_box = Gtk.Box()
        self.question_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.main_box.add(self.button_box)
        self.main_box.add(self.question_box)
        self.draw_area = Gtk.DrawingArea()

        self.number_of_questions = 0
        self.question_fields = list()
        self.question_names = list()

        self.parent = parent

        self.plus_button = Gtk.Button("Add")
        self.plus_button.connect("clicked", self.plus_clicked)
        self.button_box.add(self.plus_button)



        self.minus_button = Gtk.Button("Remove")
        self.minus_button.connect("clicked", self.minus_clicked)
        self.button_box.add(self.minus_button)

        self.submit_button = Gtk.Button("Submit")
        self.submit_button.connect("clicked", self.submit)
        self.button_box.add(self.submit_button)

        self.time_input = Gtk.Entry()
        self.time_input.set_text(str(cur_time))
        self.button_box.add(self.time_input)

        self.add_current_questions(cur_questions)

        self.draw_area.set_size_request(300, 300)
        self.show_all()


    def add_current_questions(self, cur_questions):
        for i in range(0, len(cur_questions)):
            print("(" + str(i) + ") Loading question : " + cur_questions[i].get_question())


            new_box = Gtk.Box()
            static_text = Gtk.Label("Question " + str(self.number_of_questions + 1))
            question_title = Gtk.Entry()
            question_title.set_text(cur_questions[i].get_question())
            new_box.add(static_text)
            new_box.add(question_title)

            self.question_box.add(new_box)

            self.question_fields.append(new_box)
            self.question_names.append(question_title)

            self.number_of_questions += 1
            self.show_all()

        print(" -------------------- ")


    def plus_clicked(self, widget):

        new_box = Gtk.Box()
        static_text = Gtk.Label("Question " + str(self.number_of_questions+1))
        question_title = Gtk.Entry()
        new_box.add(static_text)
        new_box.add(question_title)


        self.question_box.add(new_box)

        self.question_fields.append(new_box)
        self.question_names.append(question_title)

        self.number_of_questions += 1
        self.show_all()


    def minus_clicked(self, widget):
        if(len(self.question_fields) > 0):
            to_remove = self.question_fields[len(self.question_fields)-1]

            self.question_box.remove(to_remove)
            self.question_fields.remove(to_remove)
            self.question_names.pop()
            self.number_of_questions -= 1
            self.show_all()

    def submit(self, widget):
        try:
            self.parent.set_time(int(self.time_input.get_text()))
        except:
            self.parent.set_time(1000)

        while(not len(self.cur_questions) == 0):
            self.cur_questions.pop()
        for i in range(0, self.number_of_questions):
            print("(" + str(i) +") Adding to current: " + self.question_names[i].get_text())
            new_question = question.Question()
            new_question.set_question(self.question_names[i].get_text())

            self.cur_questions.append(new_question)
        print(" -------------------- ")
        self.destroy()