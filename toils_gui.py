import datetime
import time
import gi
import sys

import pdb
import sqlite3
import logging
import db_operations

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class TimeTracker(Gtk.Window):

    def __init__(self):

        # Top level container
        self.builder = Gtk.Builder()
        self.builder.add_from_file("layout1.glade")
        self.window = self.builder.get_object("window2")
        self.window.set_title("Toils App")
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()

        # GUI widgets
        self.btn_start = self.builder.get_object("btn_start")
        self.btn_stop = self.builder.get_object("btn_stop")
        self.lbl_time = self.builder.get_object("lbl_time")
        self.combo_client = self.builder.get_object("combo_client")
        logging.debug(
            "Combo box state: %s " % (self.combo_client.get_active_text()))
        self.combo_project = self.builder.get_object("combo_project")
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
        self.combo_client.connect("changed", self.client_drop_down_pressed)

        # Other initialisations
        self.timer_active = False
        self.duration = None
        self.update_clients_list()
        self.btn_start.set_sensitive(False)
        self.btn_stop.set_sensitive(False)

    def update_clients_list(self):
            # Update combo box without adding duplicates
            if db_operations.database_exists():
                try:
                    self.combo_client.remove_all()
                    rows = db_operations.retrieve_all_clients()
                    for client in rows:
                        self.combo_client.append_text(client[0])
                except TypeError:
                    logging.error(sys.exc_info()[1])
            else:
                logging.warning("Database not found, creating new database.")
                db_operations.create_database()
                #update_clients_list()


    def update_projects_list(self, name):
        # Update client project to display project
        self.combo_project.remove_all()
        try:
            result = db_operations.retrieve_client_details(name, "project")
            self.combo_project.append_text(result)
            self.combo_project.set_active(0)
        except:
            print(sys.exc_info()[1])



    def save_activity(self):
        # saves activity to the database
        # calculates total time spent on task
        duration = int(time.time() - self.start_time)
        #logging.debug(duration)
        client = self.combo_client.get_active_text()
        project = self.combo_project.get_active_text()
        date = datetime.date.today()
        #logging.debug(date)

        db_operations.save_work(client, project, date, duration)

    def client_drop_down_pressed(self, widget):
        current_client = self.combo_client.get_active_text()
        if current_client:
            logging.debug(str(current_client) + " selected")
            self.btn_start.set_sensitive(True)
            # Update the project name in the combo_project field
            self.update_projects_list(current_client)

    def save_button_pressed(self, widget):
        # New client window
        name = self.client_name.get_text()
        website = self.client_website.get_text()
        project = self.client_project.get_text()
        logging.debug('Name: ' + name)
        logging.debug('Website: ' + website)
        logging.debug('Project:' + project)
        logging.debug("New Client Window: Save button pressed.")

        try:
            db_operations.add_client(name, website, project)
            logging.debug("Client details successfully added to database")
        except sqlite3.OperationalError as err:
            logging.error(err)
            db_operations.create_database()
            logging.debug("New client database created")
            db_operations.add_client(name, website, project)
            logging.debug("Client details successfully added to database")

        self.update_clients_list()
        self.client_info_window_close(self)

    def client_info_window_close(self, widget):
        self.client_info_window.close()

    def new_client_window_open(self, widget):
        # Draws the Client Information Window
        # widgets are defined here because when they are defined in the
        # __init__ function of the class, they are not drawn for some reason

        logging.debug("new_client_window_open function activated")
        self.builder.add_from_file("layout1.glade")
        self.client_info_window = self.builder.get_object("window_client_info")

        # Widgets
        self.client_name = self.builder.get_object("entry_client_name")
        self.client_website = self.builder.get_object("entry_website")
        self.client_project = self.builder.get_object("entry_project")
        self.btn_cancel = self.builder.get_object("btn_cancel")
        self.btn_save = self.builder.get_object("btn_save")

        self.btn_cancel.connect("clicked", self.client_info_window_close)
        self.btn_save.connect("clicked", self.save_button_pressed)
        self.client_info_window.show_all()

    def time_function(self, time_val):
        '''Main Timer function'''

        #time_format = "{hours} Hours:{minutes} minutes:{seconds} Seconds"
        time_format = "{hours}:{minutes}:{seconds}"
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

        #start_time = start_time
        time_delta = int(time.time() - start_time)
        if self.timer_active:

            self.lbl_time.set_text(self.time_function(time_delta))
            return True
        else:
            return False

    def start_timer(self, widget):
        '''Starts the timer'''
        # TODO: Consider putting this in the __init__ constructor
        self.start_time = time.time()
        self.timer_active = not self.timer_active
        # Toggle Start and Stop button states
        self.btn_start.set_sensitive(False)
        self.btn_stop.set_sensitive(True)
        if self.timer_active is False:
            #self.button9.set_label("Start Timer")
            logging.debug("Start Button Pressed")
        else:
            #self.button9.set_label("Stop Timer")
            logging.debug("Start/Stop Button Pressed")
        GLib.timeout_add(1000, self.display_time, self.start_time)

    def stop_timer(self, widget):
        """Stops the timer"""
        self.btn_start.set_sensitive(True)
        self.btn_stop.set_sensitive(False)
        self.timer_active = False
        self.save_activity()
        logging.debug("Stop timer button pressed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')
    app = TimeTracker()
    Gtk.main()
