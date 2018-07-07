import sys
import gi


gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject


gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11
import vlc
import datetime

import save_input

class PlayerWindow(Gtk.Window):


    def __init__(self, mrl):
        # Create player window
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")
        self.connect("destroy", self.exit_window)

        # Initalise player variables
        self.player_paused = False
        self.is_player_active = False
        self.MRL = mrl





        #Recording Variables

        self.position_list = list()
        self.next_position = 1
        self.begin_time =  datetime.datetime.now()
        self.offset = 0


        #GObject.timeout_add(100, self.print_list)

    def show(self):
        self.show_all()

    def setup_objects_and_events(self):
        # BUTTONS
        self.playback_button = Gtk.Button()
        self.stop_button = Gtk.Button()

        self.play_image = Gtk.Image.new_from_icon_name(
            "gtk-media-play",
            Gtk.IconSize.MENU
        )
        self.pause_image = Gtk.Image.new_from_icon_name(
            "gtk-media-pause",
            Gtk.IconSize.MENU
        )
        self.stop_image = Gtk.Image.new_from_icon_name(
            "gtk-media-stop",
            Gtk.IconSize.MENU
        )
        self.playback_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)
        self.playback_button.connect("clicked", self.toggle_player_playback)
        self.stop_button.connect("clicked", self.stop_player)



        #SLIDER
        ad1 = Gtk.Adjustment(0, 0, 100, 5, 10, 0)
        self.slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1)
        self.slider.set_digits(0)
        self.slider.set_hexpand(True)
        self.slider.set_valign(Gtk.Align.START)
        #self.slider.connect("value-changed", self.slider_moved)

        #QUESTION
        self.question_label = Gtk.Label("this is the question?")



        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(500, 500)

        self.draw_area.connect("realize", self._realized)

        self.hbox = Gtk.Box(spacing=6)
        self.hbox.pack_start(self.playback_button, True, True, 15)



        self.sliderbox = Gtk.Box()
        self.sliderbox.pack_start(self.slider, True, True, 0)

        self.questionbox = Gtk.Box()
        self.questionbox.pack_start(self.question_label, True, True, 0)


        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        self.vbox.pack_start(self.sliderbox, False, False, 0)
        self.vbox.pack_start(self.questionbox, False, False, 0)


    # This may do nothing, unsure as of yet.
    def stop_player(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)


    def toggle_player_playback(self, widget, data=None):
        if self.is_player_active == False and self.player_paused == False:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.is_player_active = True

        elif self.is_player_active == True and self.player_paused == True:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.player_paused = False

            # This restarts the recording after a pause.
            print "starting player"
            self.record_slider()

        elif self.is_player_active == True and self.player_paused == False:
            self.player.pause()
            self.playback_button.set_image(self.play_image)
            self.player_paused = True
        else:
            pass


    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        self.player.set_mrl(self.MRL)
        self.player.play()
        self.playback_button.set_image(self.pause_image)
        self.is_player_active = True

        # This begins the recording of the slider.
        self.record_slider()
        print "video has begun"

    def record_slider(self):
        # This function is called every 100ms if the video state is playing.
        # This function records the value of the slider at each tick, or initiates the saving process if the video has ended.
        if(str(self.player.get_state()) == "State.Paused"):
            self.offset = self.next_position
            pass
        elif(str(self.player.get_state()) == "State.Playing"):
            self.position_list.append(int(self.slider.get_value()))
            GObject.timeout_add(100, self.record_slider)
            print str(int(self.slider.get_value()))
        elif(str(self.player.get_state()) == "State.Ended"):
            self.save_list()
        else:
            GObject.timeout_add(100, self.record_slider)



    # This is for testing purposes only!
    def print_list(self):
        print self.position_list

    # This is the link between the player and the saving library.
    def save_list(self):
        save_input.save_input(self, self.position_list)

    # This is called to released the player when the player exits the window.
    def exit_window(self):
        window.player.stop()
        window.vlcInstance.release()



