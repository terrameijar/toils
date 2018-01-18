import datetime
import time
import gi
import pdb
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class TimeTracker(Gtk.Window):

    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file("layout1.glade")
        self.window = self.builder.get_object("window2")
        self.window.set_title("Toils App")
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()

        # GUI Widgets
        self.btn_start = self.builder.get_object("btn_start")
        self.btn_stop = self.builder.get_object("btn_stop")
        self.lbl_time = self.builder.get_object("lbl_time")
        self.lbl_task_name = self.builder.get_object("lbl_taskName")
        self.entry_task_name = self.builder.get_object("entry_activity")

        # Main menu container
        self.main_menubar = self.builder.get_object("menubar2")

        # Main menu items
        self.file_menu = self.builder.get_object("menuitem_file")
        self.edit_menu = self.builder.get_object("menuitem_edit")

        # Drop Down Menu items
        self.file_new = self.builder.get_object("menuitem_file_new")
        self.edit_prefs = self.builder.get_object("menuitem_edit_pref")

        # Widget-Signal connections
        self.btn_start.connect("clicked", self.start_timer)
        self.btn_stop.connect("clicked", self.stop_timer)
        self.file_new.connect("activate", self.new_client_window_open)

        # Other initialisations
        self.timer_active = False


    def save_button_pressed(self, widget):
        logging.debug(self.client_name.get_text())
        # TODO: Save client in a DB
        fobj = open('time_data.txt', 'a+')
        fobj.write(self.client_name.get_text())
        fobj.write('\n')
        fobj.close()


    def client_info_window_close(self, widget):
        self.client_info_window.close()

    def new_client_window_open(self, widget):
        # Draws the Client Information Window
        logging.debug("new_client_window_open function activated")
        #pdb.set_trace()
        self.builder.add_from_file("layout1.glade")
        self.client_info_window = self.builder.get_object("window_client_info")

        # Widgets
        self.client_name = self.builder.get_object("entry_client_name")
        self.btn_cancel = self.builder.get_object("btn_cancel")
        self.btn_save = self.builder.get_object("btn_save")
        self.btn_cancel.connect("clicked", self.client_info_window_close)
        self.btn_save.connect("clicked", self.save_button_pressed)
        self.client_info_window.show_all()

    def time_function(self, time_val):
        '''Main Timer function'''

        time_format = "{hours} Hours:{minutes} minutes:{seconds} Seconds"
        time_delta = time_val

        mins = int(time_delta / 60)
        hours = int(time_delta / 3600)
        days = int(time_delta / 86400)
        seconds = int(time_delta) - mins * 60
        if seconds >= 60:
            seconds = 0
        if mins >= 60:
            mins = mins - hours * 60
        if hours >= 24:
            hours = hours - days * 24

        # Make values zero padded
        h,m,s = '{:02}'.format(hours), '{:02}'.format(mins), '{:02}'.format(seconds)
        return time_format.format(hours=h, minutes=m, seconds=s)


    def display_time(self, start_time):
        '''Update GUI with elapsed time'''

        start_time = start_time
        time_delta = int(time.time() - start_time)
        self.lbl_task_name.set_text(self.entry_task_name.get_text())
        if self.timer_active:

            self.lbl_time.set_text(self.time_function(time_delta))
            return True
        else:
            return False

    def start_timer(self, widget):
        '''Starts the timer'''

        self.start_time = time.time()
        self.timer_active = not self.timer_active
        if self.timer_active is False:
            #self.button9.set_label("Start Timer")
            print("Start Button Pressed")
        else:
            #self.button9.set_label("Stop Timer")
            print("Start/Stop button pressed")
        GLib.timeout_add(1000, self.display_time, self.start_time)

    def stop_timer(self, widget):
        """Stops the timer"""
        self.timer_active = False
        print("Stop timer button pressed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')
    app = TimeTracker()
    Gtk.main()
