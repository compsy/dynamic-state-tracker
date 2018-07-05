

import gi
import select_file
import player
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GdkX11', '3.0')


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")

        self.selected_file = None

        self.start_button = Gtk.Button("        Start        ")
        self.start_button.connect("clicked", self.start)


        self.select_video_button = Gtk.Button("Select video")
        self.select_video_button.connect("clicked", self.select_video)


        self.question_settings_button = Gtk.Button("Set questions")
        self.question_settings_button.connect("clicked", self.question_settings)


        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(300, 100)

        self.hbox = Gtk.Box(spacing=6)
        self.hbox.pack_start(self.start_button, True, True, 0)
        self.hbox.pack_start(self.select_video_button, True, True, 0)
        self.hbox.pack_start(self.question_settings_button, True, True, 0)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(Gtk.Label("Dynamic State Tracker"), True, True, 0)

        self.selected_label = Gtk.Label("Video selected: ")
        self.vbox.pack_start(self.selected_label, True, True, 0)
        self.add(self.vbox)


        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)

    def start(self, widget):
        if self.selected_file is None:
            print("Failed: No file selected")
        else:
            print("Opening " + self.selected_file)
            window = player.PlayerWindow(self.selected_file)
            window.setup_objects_and_events()
            window.show()



    def select_video(self, widget):
        print("Selecting video")
        win = select_file.FileChooserWindow(self)
        win.show_all()

    def question_settings(self, widget):
        print("settings")


    def update_selected(self, new_selected):
        self.selected_file = new_selected
        last_part_of_path = new_selected.split("/")
        self.selected_label.set_text("Video selected: " + last_part_of_path[len(last_part_of_path)-1])

mainWindow = MainWindow()
mainWindow.show_all()
Gtk.main()