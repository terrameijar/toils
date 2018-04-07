import os
import os.path
import sqlite3


# TODO: Add database operations into this file
# TODO: Add code to modify database records
# TODO: User must be able to update/delete clients
# TODO: User must be able to retrieve clients
# TODO: Handle missing database problem.
# TODO: Consider using only one function to handle SQL operations
# TODO: Add table to keep track of time user has spent on each client
# TODO: Add code to create the user table
# TODO: Add Jane Doe as the first client in the test database

DATABASE = 'client_data/clients.db'
# DATABASE = 'client_data/clients_staging.db'
filepath = 'client_data/'
database_name = "clients.db"
#filename = os.path.join(filepath, 'test.db')

def create_database():
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    #filename = os.path.join(filepath, 'clients_staging.db')
    filename = os.path.join(filepath, database_name)
    with sqlite3.connect(filename) as conn:
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS "
            "clients (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, "
            "client_website TEXT,project TEXT NOT NULL)"
        )

        c.execute(
            "CREATE TABLE IF NOT EXISTS "
            "user (task_id INTEGER, client_id INTEGER,client_name TEXT, project"
            " TEXT, task_date TEXT, duration	NUMERIC, PRIMARY KEY(task_id))"
        )
    assert os.path.exists(filename)

def destroy_database():
    pass

def database_exists():
    return os.path.exists(DATABASE)

def create_db_connection(db_name):
    pass
    # connect to the database

def add_client(name, website, project, rate=0):
    # TODO: Add code that allows adding rate to database
    client = (name, website, project)
    # Add this customer to database
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO clients(client_name, client_website, project) "
                "VALUES (?,?,?)", client
            )
            conn.commit()
    except sqlite3.OperationalError as err:
        print(err)

def retrieve_client_details(name, detail):
    # Return a particular detail about the client
    operation = {"id": 0, "name": 1, "website": 2, "project": 3}

    # Make a single element tuple to avoid SQL injection
    name = (name,)
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM clients WHERE client_name =?", name)
            result = c.fetchone()
            return result[operation[detail]]

    except sqlite3.OperationalError as err:
        print("An error occurred", err)

def modify_client(name):
    pass

def delete_client(name):
    pass
    # remove this client from database

def retrieve_single_client(name):
    # Retrieves all the details of named client
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute("SELECT client_name, client_website \
               FROM clients WHERE client_name = name")
            client_details = c.fetchall()
            return client_details
    except sqlite3.OperationalError as err:
        print(err)

def retrieve_client_list():
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT client_name FROM clients")
            rows = c.fetchall()
            return rows
    except sqlite3.OperationalError as err:
        print(err)

def retrieve_all_clients():
    # Retrieve the details of all the clients
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT client_name, client_website, project FROM clients")
            rows = c.fetchall()
            return rows
    except sqlite3.OperationalError as err:
        print(err)

### Functions relating to the user's work records ###

def save_work(client, project, date, duration):
    # Client ID is the PK in clients table
    client_id = retrieve_client_details(client, "id")
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            work = (client_id, client, project, date, duration)
            c.execute(
                "INSERT INTO user "
                "(client_id, client_name, project, task_date, duration)"
                " VALUES (?,?,?,?,?)", work
            )
            conn.commit()
    except sqlite3.OperationalError as err:
        print(err)

def retrieve_user_work_record():
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT client_name, project, task_date, duration FROM user"
            )
            rows = c.fetchall()
            return rows
    except sqlite3.OperationalError as err:
        print(err)


if __name__ == '__main__':
    create_database()
