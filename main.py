import gi
import select_file
import player
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GdkX11', '3.0')
import question
import settings
import review
class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Dynamic State Tracker")
        self.selected_file = None
        self.questions = list()
        self.time_interval = 100


        first_question = question.Question()
        first_question.question = "How confident were you?"
        first_question.type = "slider"
        self.questions.append(first_question)

        second_question = question.Question()
        second_question.question = "How scared were you?"
        second_question.type = "slider"
        self.questions.append(second_question)


        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(10, 50)

        # Create and assign action to start button
        self.start_button = Gtk.Button("        Start        ")
        self.start_button.connect("clicked", self.start)

        # Create and assign action to select video button
        self.select_video_button = Gtk.Button("Select video")
        self.select_video_button.connect("clicked", self.select_video)

        # Create and assign action to question settings button
        self.question_settings_button = Gtk.Button("Set questions")
        self.question_settings_button.connect("clicked", self.question_settings)

        self.analyse_button = Gtk.Button("Analyse Data")
        self.analyse_button.connect("clicked", self.analyse_data)

        # Create gtk box and pack all buttons into it. This box is at the bottom of the application
        self.hbox = Gtk.Box(spacing=6)
        self.hbox.pack_start(self.start_button, True, True, 0)
        self.hbox.pack_start(self.select_video_button, True, True, 0)
        self.hbox.pack_start(self.question_settings_button, True, True, 0)
        self.hbox.pack_start(self.analyse_button, True, True, 0)

        # Create gtk box containing title and video selected information and the gtk box above
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(Gtk.Label("Dynamic State Tracker"), True, True, 0)
        self.selected_label = Gtk.Label("Video selected: ")
        self.vbox.pack_start(self.selected_label, True, True, 0)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)


    def start(self, widget):
        # Check to see if any file is selected (still need to check if file is a video file)
        if self.selected_file is None:
            print("Failed: No file selected")
        else:
            print("Opening " + self.selected_file)

            window = player.PlayerWindow(self.selected_file, self.questions, self.time_interval)
            window.setup_objects_and_events()
            window.show()

    def select_video(self, widget):
        print("Selecting video")
        win = select_file.FileChooserWindow(self, "video")


    def question_settings(self, widget):
        print("settings to be added")
        settings_window = settings.SettingsWindow(self, self.questions, self.time_interval)



    def analyse_data(self, widget):
        win =  select_file.FileChooserWindow(self, "save")


    def set_time(self, time):
        self.time_interval = time

    def update_selected(self, type, new_selected):
        # This function is used to update the variable and label for selected files.
        if(type == "video"):
            self.selected_file = new_selected
            last_part_of_path = new_selected.split("/")
            self.selected_label.set_text("Video selected: " + last_part_of_path[len(last_part_of_path)-1])
        elif(type == "save"):
            review.ReviewWindow(self, new_selected)


# This is the beginning of the application.
mainWindow = MainWindow()
mainWindow.show_all()
Gtk.main()