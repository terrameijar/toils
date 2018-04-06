import gi
import sqlite3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class CellRendererTextWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Time Tracker completed work")
        self.set_default_size(400,300)
        self.set_border_width(20)

        # Setting up the grid in which elements are to be added.
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # Setting up window widgets that will be used to display the info
        self.list_store_work_record = Gtk.ListStore(int, int, str, str, str, float)
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)

        self.cbo_text = Gtk.ComboBoxText()
        self.cbo_text.append_text("Select a client")
        self.cbo_text.set_active(0)
        self.btn_export = Gtk.Button("Export to Excel")
        self.btn_export.connect("clicked", self.on_button_click)
        self.treeview = Gtk.TreeView(model=self.list_store_work_record)

        self.renderer_text = Gtk.CellRendererText()
        self.column_text = Gtk.TreeViewColumn(
            "Project Title", self.renderer_text, text=0)
        self.treeview.append_column(self.column_text)
        self.renderer_editable_client = Gtk.CellRendererText()
        self.renderer_editable_client.set_property("editable", True)
        self.column_editable_client = Gtk.TreeViewColumn(
            "Client",self.renderer_editable_client, text=1)
        self.renderer_client_name = Gtk.CellRendererText()
        self.renderer_project = Gtk.CellRendererText()
        self.renderer_date = Gtk.CellRendererText()
        self.renderer_hours = Gtk.CellRendererText()

        self.column_client_name = Gtk.TreeViewColumn(
            "Client Name", self.renderer_client_name, text=2)
        self.column_project = Gtk.TreeViewColumn(
            "Project",self.renderer_project, text=3)
        self.column_date = Gtk.TreeViewColumn(
            "Date", self.renderer_date, text=4)
        self.column_hours = Gtk.TreeViewColumn(
            "Hours", self.renderer_hours, text=5)
        self.treeview.append_column(self.column_editable_client)
        self.treeview.append_column(self.column_client_name)
        self.treeview.append_column(self.column_project)
        self.treeview.append_column(self.column_date)
        self.treeview.append_column(self.column_hours)

        self.scrolled_window.add(self.treeview)
        # List of work records
        self.work_record = self.get_details_of_work_done()


    def populate_treeview(self):
        #rows = self.get_details_of_work_done()
        for index,item in enumerate(self.work_record):
            self.list_store_work_record.append(item)

        #self.scrolled_window.add(self.treeview)

        #self.btn_export.connect("clicked", self.on_button_click, self.work_record)

        clients = self.get_clients_list()
        for client in clients:
            self.cbo_text.append_text(client[0])
        self.grid.attach(self.scrolled_window,0,0,8,10)
        self.grid.attach_next_to(self.btn_export, self.scrolled_window, Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.cbo_text, self.btn_export, Gtk.PositionType.RIGHT,1,1)

    def get_details_of_work_done(self, name=None):
        with sqlite3.connect("client_data/clients.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM user")
            rows = c.fetchall()
            return rows

    def get_clients_list(self):
        with sqlite3.connect("client_data/clients.db") as conn:
            c = conn.cursor()
            c.execute("SELECT client_name from clients")
            clients = c.fetchall()
            return clients

    def export_work_record(self, work_record):
        print(work_record)
        with open("test.txt", "w") as fobj:
            for record in work_record:
                record = str(record)
                fobj.write(record.strip("()"))
                fobj.write("\n")



    def on_button_click(self, widget):
        # TODO: handle exporting to excel sheet here.
        print("work record length:",len(self.work_record))
        if not self.cbo_text.get_active() == 0:
            print("Selected client: " + self.cbo_text.get_active_text())
            self.export_work_record(self.work_record)

    def text_edited(self, widget, path, text):
        self.list_store_work_record[path][1] = text

win = CellRendererTextWindow()
win.connect("delete-event", Gtk.main_quit)
win.populate_treeview()
win.show_all()
Gtk.main()
