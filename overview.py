from functools import reduce
import csv
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import db_operations
import invoices


class TreeViewFilterWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Client List TreeView Filter")
        self.set_default_size(400, 300)
        print(self.get_size())
        self.set_border_width(10)

        # setting up the grid in which elements will go
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # Get timesheets from database
        work_record = db_operations.retrieve_user_work_record()

        # Creating the ListStore model
        self.work_record_liststore = \
            Gtk.ListStore(str, str, str, float)
        for record in work_record:
            self.work_record_liststore.append(list(record))
        self.current_filter_client = None

        # Creating Filter, feeding it with the liststore model
        self.client_filter = self.work_record_liststore.filter_new()
        # setting the filter function
        self.client_filter.set_visible_func(self.client_filter_func)

        # creating the TreeView, making it use the
        # filter as a model and adding columns
        self.treeview = Gtk.TreeView.new_with_model(self.client_filter)
        self.treeview_selection = self.treeview.get_selection()
        self.treeview_selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.columns = ["Client Name", "Project", "Date", "Hours"]
        for i, column_title in enumerate(self.columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # combo box to filter records by client
        self.cbo_client = Gtk.ComboBoxText()
        self.cbo_client.append_text("All Clients")
        self.cbo_client.set_active(0)
        self.btn_export = Gtk.Button("Export TimeSheet")
        self.btn_export.connect("clicked", self.export_timesheet, self.client_filter)
        self.btn_export.set_sensitive(False)
        self.select_all = Gtk.CheckButton("Select All")
        self.select_all.connect("toggled", self.on_check_btn_toggle)

        clients_list = self.get_clients()
        for client in clients_list:
            self.cbo_client.append_text(client[0])
        self.cbo_client.connect("changed", self.on_combo_selection_changed)

        # setting up layout, TreeView goes into a window and combo box text
        #  goes below it
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 3, 12)
        self.grid.attach_next_to(self.cbo_client, self.scrollable_treelist,
                                 Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.btn_export, self.cbo_client, Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.select_all, self.btn_export, Gtk.PositionType.RIGHT, 1,1)
        self.scrollable_treelist.add(self.treeview)
        self.show_all()
        self.get_clients()


    def client_filter_func(self, model, iter, data):
        """Tests if the client in the row is the one in the filter"""
        if self.current_filter_client is None or \
                        self.current_filter_client == "All Clients":
            return True
        else:
            return model[iter][0] == self.current_filter_client


    def on_combo_selection_changed(self, widget):
        # Updates the treeview to show work done for the selected client

        self.current_filter_client = widget.get_active_text()
        if self.current_filter_client != "All Clients":
            self.btn_export.set_sensitive(True)
        else:
            self.btn_export.set_sensitive(False)

        # If client changed, uncheck the select all checkbox and refresh filter
        self.select_all.set_active(False)
        self.client_filter.refilter()

    def on_check_btn_toggle(self, widget):
        toggled = self.select_all.get_active()
        if toggled:
            self.treeview_selection.select_all()
        else:
            self.treeview_selection.unselect_all()


    def get_clients(self):
        return db_operations.retrieve_client_list()

    def export_timesheet(self, widget, data):
        # This function allows the user to select the work records they want
        # to export to the spreadsheet or database.
        time_sheet = []
        model, selected_rows = self.treeview_selection.get_selected_rows()
        if selected_rows != None:
            for row in selected_rows:
                time_sheet.append(model[row][0:])

        # Save the names of the project(s) the user did for client
        projects = {record[1] for record in time_sheet}

        # Calculate out how much time the user spent working for client
        hours = [work_record[3] for work_record in time_sheet]
        total_hours = int(reduce((lambda x, y: x + y), hours))

        # Determine the start and end dates
        start_date = time_sheet[0][2]  # Get date in first record
        end_date = time_sheet[-1][2]   # Get date in the last record


        try:
            with open("work_record.txt", "a+") as fobj:
                for record in  time_sheet:
                    for item in record:
                        fobj.write(str(item) + " ")
                    fobj.write("\n")

            with open("work_record.csv", "w") as fobj:
                output_writer = csv.writer(fobj)
                for record in time_sheet:
                    output_writer.writerow(record)
        except IOError:
            print("IO Error")

        invoices.generate_excel_invoice(start_date,end_date,projects, total_hours)
        return time_sheet, projects, start_date, end_date, total_hours


if __name__ == "__main__":
    win = TreeViewFilterWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
