import os
import shutil
import os.path
import unittest
import db_operations
import toils_gui
import overview
import sqlite3
from faker import Faker
import pdb



class TestTimeTracker(unittest.TestCase):
    fake = Faker()

    db_operations.DATABASE = "client_data/test.db"
    db_operations.database_name = "test.db"
    TEST_DB = db_operations.DATABASE
    TEST_DB_NAME = db_operations.database_name
    filename = "client_data/test.db"
    name, website, project = fake.name(), fake.domain_name(), fake.bs().split()[2]

    @classmethod
    def setUpClass(cls):
        db_operations.create_database()

    def test_that_db_file_can_be_created(self):
        #db_operations.create_database()
        #self.assertTrue(os.path.exists(self.TEST_DB_NAME))
        self.assertTrue(os.path.exists(self.TEST_DB))

    def test_db_contains_client_table(self):
        with sqlite3.connect(self.TEST_DB) as connection:
            c = connection.cursor()
            try:
                c.execute("SELECT 1 from CLIENTS limit 1;")
            except sqlite3.OperationalError as err:
                self.fail(err)

    def test_db_contains_user_table(self):
        with sqlite3.connect(self.TEST_DB) as connection:
                c = connection.cursor()
                try:
                    c.execute("SELECT 1 from USER limit 1;")
                except sqlite3.OperationalError as err:
                    self.fail(err)

    @unittest.skip("Not been implemented yet.")
    def test_that_db_can_be_destroyed(self):
        self.fail("You have not coded this!")

    def test_adding_new_client(self):
        try:
            #db_operations.add_client("Jane Doe", "example.com", "FooBar")
            db_operations.add_client(self.name, self.website, self.project)
        except sqlite3.OperationalError as err:
            self.fail(err)

    def test_retrieve_client_website(self):
        try:
            site = db_operations.retrieve_client_details(self.name, "website")
            self.assertEqual(site, self.website)
        except sqlite3.OperationalError as err:
            self.fail(err)

    def test_retrieve_client_project(self):
        project = db_operations.retrieve_client_details(self.name, "project")
        self.assertEqual(project, self.project)

    def test_retrieve_client_id(self):
        client_id = db_operations.retrieve_client_details(self.name, "id")
        self.assertEqual(client_id, 2)

    def test_modify_client_name(self):
        pass

    def test_modify_client_project(self):
        pass

    def test_modify_client_website(self):
        pass

    def test_save_work(self):
        pass

    def test_retrieve_all_clients(self):
        pass

    def test_delete_client(self):
        pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.TEST_DB)
        except FileNotFoundError as err:
            print(err)

class TestUI(unittest.TestCase):
    fake = Faker()

    db_operations.DATABASE = "client_data/test.db"
    db_operations.database_name = "test.db"
    TEST_DB = db_operations.DATABASE
    TEST_DB_NAME = db_operations.database_name
    name, website, project = fake.name(), fake.domain_name(), fake.bs().split()[2]
    db_operations.create_database()
    db_operations.add_client(name, website, project)
    app = toils_gui.TimeTracker()

    @classmethod
    def setUpClass(cls):

        filename = "client_data/test.db"
        #db_operations.create_database()
        #db_operations.add_client(cls.name, cls.website, cls.project)
        #self.app = toils_gui.TimeTracker()

    def test_client_combo_box_is_not_empty(self):
        pass

    def test_that_time_label_does_not_display_time_on_startup(self):
        self.assertEqual(self.app.lbl_time.get_text(), "Current time")

    def test_start_button_is_disabled_on_startup(self):
        self.assertFalse(self.app.btn_start.get_sensitive())

    def test_stop_button_is_disabled_on_startup(self):
        self.assertFalse(self.app.btn_stop.get_sensitive())

    def test_client_combo_box_displays_nothing_on_startup(self):
        self.assertEqual(self.app.combo_client.get_active(), -1)

    def test_project_combo_box_is_updated_when_client_selected(self):
        self.app.combo_client.set_active(1)
        self.assertTrue(self.app.combo_project.get_sensitive())

    def test_start_button_gets_activated_when_client_selected(self):
        self.app.combo_client.set_active(0)
        self.assertTrue(self.app.btn_start.get_sensitive())

    def test_client_combo_displays_correct_tooltip(self):
        self.assertEqual(
            self.app.combo_client.get_tooltip_text(),
            "List of clients you do work for."
        )

    def test_that_combo_project_shows_correct_project_for_each_client(self):
        self.app.combo_client.set_active(0)
        client_name = self.app.combo_client.get_active_text()
        project = self.app.combo_project.get_active_text()
        self.assertEqual(client_name, self.name)
        self.assertEqual(project, self.project)

    def tearDown(self):
        self.app.btn_start.set_sensitive(False)
        self.app.combo_client.set_active(-1)

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.TEST_DB)
        except FileNotFoundError as err:
            print(err)

class TestOverview(unittest.TestCase):

    def test_client_dropdown_displays_correct_clients(self):
        self.overview_window = overview.TreeViewFilterWindow()
        active_client = self.overview_window.cbo_client.get_active()
        self.assertEqual(active_client, "All Clients")



if __name__ == "__main__":
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()
