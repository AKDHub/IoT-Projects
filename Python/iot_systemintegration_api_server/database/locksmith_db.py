import os.path
import sqlite3
from sqlite3 import Error
import os

PATH_DB_TABLES = os.path.abspath(os.path.dirname(__file__))


class SqliteDB:
    """ Instance of a Sqlite Database. """
    @staticmethod
    def create_connection(path: str):
        """Open path as a database"""
        connection = None
        try:
            # Försöker du koppla till en fil som inte finns,
            # skapar sqlite3.connect en ny fil enligt "path"
            connection = sqlite3.connect(path)
            # print("Connection to SQLite DB successful!")
        except Error as e:
            print(f"The error {e} occurred!")
        return connection

    @staticmethod
    def db_exists(db_name: str) -> bool:
        """
        Checks if database with name 'db_name' exists or not.

        :param db_name: name of the database to check.
        :return: true if database exists otherwise false.
        """
        return os.path.isfile(os.path.join(PATH_DB_TABLES, db_name + ".db"))

    @staticmethod
    def execute_read_query(connection, query: str, limit: int = None):
        """Use this function to read data from database"""
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            if limit:
                result = cursor.fetchmany(limit)
            else:
                result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error {e} occurred!")

    @staticmethod
    def execute_write_query(connection, query: str):
        """Executes a query on a database connection. """
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except Error as e:
            print(f"The error {e} occurred!")

    def open_connection(self, db: str):
        return self.create_connection(os.path.join(PATH_DB_TABLES, db + ".db"))

    def execute_query(self, query: str,
                      select: bool = False,
                      insert: bool = False,
                      update: bool = False,
                      delete: bool = False,
                      limit: int = None):
        """
        Executes a database sqlite query.

        :param query: Query to execute
        :param select: Set to true if query is SELECT
        :param insert: Set to true if query is INSERT
        :param update: Set to true if query is UPDATE
        :param delete: Set to true if query is DELETE
        :param limit: Set a limit if SELECT is used
        :return: Result of the executed query
        """
        results = None
        connection = self.open_connection(self.db_name)
        if insert or update or delete:
            self.execute_write_query(connection=connection, query=query)
        elif select:
            results = self.execute_read_query(connection=connection, query=query, limit=limit)
        connection.close()

        if select:
            return results


class LocksmithDB(SqliteDB):
    """
    Instance of a Locksmith Database.
    """
    def __init__(self):
        self.db_name = "locksmith"
        if not self.db_exists(self.db_name):
            db_connect = self.open_connection(self.db_name)
            self.init_locksmith_db(db_connect)
            db_connect.close()

    def init_locksmith_db(self, connection):
        """
        initiate Locksmith database with tables and relations.

        :param connection: Database connection
        :return: No returning argument
        """
        query = """
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        regtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        name TEXT NOT NULL,
        email TEXT,
        door_code INT UNIQUE NOT NULL
        );
        """

        self.execute_write_query(connection=connection, query=query)

        query = """
        CREATE TABLE IF NOT EXISTS Doors(
        id INTEGER PRIMARY KEY,
        adress TEXT NOT NULL,
        room TEXT NOT NULL
        );
        """

        self.execute_write_query(connection=connection, query=query)

        query = """
                CREATE TABLE IF NOT EXISTS UserDoors(
                username TEXT REFERENCES Users(username),
                door_id INTEGER REFERENCES Doors(id),
                code INT REFERENCES Users(door_code)
                );
                """

        self.execute_write_query(connection=connection, query=query)

        query = """
        CREATE TABLE IF NOT EXISTS Loggs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        door_id INTEGER REFERENCES Doors(id),
        username TEXT NOT NULL,
        event TEXT NOT NULL,
        access BOOL NOT NULL,
        entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL 
        );
        """

        self.execute_write_query(connection=connection, query=query)

    def valid_code(self, door_id, door_code):
        """
        Validates door code for door with ID 'door_id'.

        :param door_id: ID of a door.
        :param door_code: Door code to check.
        :return: True if door_id has valid code door_code, otherwise false.
        """
        query = f"""SELECT * FROM UserDoors WHERE door_id={door_id} AND code={door_code}"""
        users = self.execute_query(query=query, select=True)
        print("length of rows = " + str(len(users)))
        if len(self.execute_query(query=query, select=True)) <= 0:
            print("Returning False")
            return False, 'Unknown'
        print("Returning True")
        return True, users[0][0]

    def get_user_doors(self, username) -> dict:
        """
         Return all doors belonging to user 'username'

        :param username: Username of the door owner.
        :return: Dictionary of all door ID's belonging to username.
        """
        query = f"""SELECT * FROM UserDoors WHERE username='{username}'"""
        doors = self.execute_query(query=query, select=True)
        doors_dict = {'doors': []}
        for door in doors:
            doors_dict['doors'].append(door[1])
        return doors_dict

    def get_loggs(self, door_id) -> dict:
        """
        Return all loggs for Door with ID 'door_id'

        :param door_id: ID of the door to get loggs from.
        :return: Dictionary with array of logg entries.
        """
        query = f"""SELECT * FROM Loggs WHERE door_id={door_id}"""
        loggs = self.execute_query(query=query, select=True)
        loggs_dict = {'loggs': []}
        for logg in loggs:
            loggs_dict['loggs'].append({'username': logg[2],
                                        'event': logg[3],
                                        'access': logg[4],
                                        'entry_time': logg[5]})
        return loggs_dict

    def logg_attempted_access(self, door_id, username, source):
        """
        Loggs attempted access on door with door_id and username, in database.

        :param door_id: ID of door.
        :param username: Name of User that attempted access.
        :param source: From where was the attempted acccess.
        :return: No returning argument.
        """
        access = "TRUE"
        if username == 'Unknown':
            access = "FALSE"
        query = f"""INSERT INTO Loggs(door_id, username, event, access) 
                    VALUES({door_id}, '{username}', 'Attempted Access: {source}', {access})"""
        print(query)
        self.execute_query(query=query, insert=True)
