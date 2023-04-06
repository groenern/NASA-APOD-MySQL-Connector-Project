import mysql.connector

class MySQLConnector:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                passwd=self.password,
                database=self.database
            )
            print("MySQL connection successful")
        except mysql.connector.Error as error:
            print(f"Error: '{error}'")
            raise Exception(f"Error connecting to MySQL: '{error}'")

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, values=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)  # pass the values as a tuple here
            self.connection.commit()
        except Exception as error:
            self.connection.rollback()
            raise Exception(f"Error executing query: '{error}'")
        finally:
            cursor.close()

    def read_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            #print(result)
            return result
        except mysql.connector.Error as error:
            print(f"Error: '{error}'")
            raise Exception(f"Error reading query: '{error}'")
        finally:
            cursor.close()