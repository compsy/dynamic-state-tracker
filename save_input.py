import sys
import gi
import jsonify
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def save_input(parent, list):
    dialogWindow = Gtk.MessageDialog(parent,
                                     Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                     Gtk.MessageType.QUESTION,
                                     Gtk.ButtonsType.OK,
                                     "Enter in the name of your save")

    dialogWindow.set_title("Save your input")

    dialogBox = dialogWindow.get_content_area()
    userEntry = Gtk.Entry()
    userEntry.set_size_request(250, 0)
    dialogBox.pack_end(userEntry, False, False, 0)

    dialogWindow.show_all()
    dialogWindow.run()
    text = userEntry.get_text()
    dialogWindow.destroy()

    print text
    save_string = format_save(list)

    f = open("saves/" + text+".txt", "w+")
    f.write(save_string)
    f.close()

def format_save(list):
    return json.dumps(list)