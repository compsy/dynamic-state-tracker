import gi
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def save_input(parent, questions):
    # This is the pop up requesting input
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

    f = open("saves/" + text + ".txt", "w+")

    # Format data (Simple now but will become more complex)
    for i in range(0, len(questions)):
        save_string = format_save(questions[i])
        f.write(save_string)
        f.write("//\n")

    # Create, write to and then close file. (Should be using try statement here!)


    f.close()

def format_save(question):

    name = question.get_question()
    data = json.dumps(question.get_data())

    return_value = name + " - " + data

    return return_value