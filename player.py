import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11

import vlc

#MRL = ""


class PlayerWindow(Gtk.Window):

    def __init__(self, mrl):
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")
        self.player_paused = False
        self.is_player_active = False
        self.connect("destroy", Gtk.main_quit)
        self.MRL = mrl

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
        self.slider.connect("value-changed", self.slider_moved)

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


    def slider_moved(self, event):
        media = self.player.get_media()
        print media.get_state()
        print media.get_stats()
        #self.question_label.set_text(str(int(self.slider.get_value())))
        #print("slider moved")


if __name__ == '__main__':
    if not sys.argv[1:]:
        print "Exiting \nMust provide the MRL."
        sys.exit(1)
    if len(sys.argv[1:]) == 1:
        MRL = sys.argv[1]
        window = PlayerWindow()
        window.setup_objects_and_events()
        window.show()
        Gtk.main()
        window.player.stop()
        window.vlcInstance.release()