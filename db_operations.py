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

DATABASE = 'client_data/clients.db'

def create_database():
    filepath = 'client_data/'
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    filename = os.path.join(filepath, 'clients.db')
    with sqlite3.connect(filename) as conn:
        c = conn.cursor()
        c.execute(
            """CREATE TABLE clients (client_name TEXT, client_website TEXT,
               project TEXT NOT NULL, PRIMARY KEY(client_name))
               """)
    assert os.path.exists(filename)

def destroy_database():
    pass

def create_db_connection(db_name):
    pass
    # connect to the database

def add_client(name, website, project, rate=0):
    # TODO: Add code that allows adding rate to database
    client = (name, website, project)
    # Add this customer to database
    # TODO: Add a try/except clause to catch db not found error
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO clients VALUES (?,?,?)", client)
            conn.commit()
    except:
        # except OperationalError:
        pass

def retrieve_client_details(name):
    # Return the project details of one client
    
    # Make a single element tuple to avoid SQL injection
    name = (name,)
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT project FROM clients WHERE client_name =?", name)
            project = c.fetchone()
            return project[0]

    except sqlite3.OperationalError as err:
        # except OperationalError:
        print("An error occurred", err)

def modify_client(name):
    pass

def delete_client(name):
    pass
    # remove this client from database

def retrieve_all_clients():
    # Retrieve the details of all the clients
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT client_name, client_website, project FROM clients")
            rows = c.fetchall()
            return rows
    except sqlite3.OperationalError:
        print("Something went wrong!!")




if __name__ == '__main__':
    create_database()
