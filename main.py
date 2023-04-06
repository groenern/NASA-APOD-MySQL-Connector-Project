import requests
from PIL import Image
import mysql.connector
from datetime import datetime
from pprint import PrettyPrinter
import urllib.request

pp = PrettyPrinter()

class NASAImage:
    def __init__(self, image):
        self.date = datetime.strptime(image.get('date', ''), '%Y-%m-%d').date()
        self.hdurl = image.get('hdurl', '')
        self.url = image.get('url', '')
        self.title = image.get('title', '')
        self.media_type = image.get('media_type', '')
        self.copyright = image.get('copyright', '')
        self.service_version = image.get('service_version', '')

class JsonLoader:
    URL_APOD = "https://api.nasa.gov/planetary/apod"
    api_key = 'CD2SnMYuuP4QRtl0BchenBIF1lMFnHwbonpPclNf'

    def __init__(self, count):
        self.count = count
        self.params = {
            'api_key':self.api_key,
            'count':self.count
        }

        self.images = requests.get(self.URL_APOD,params=self.params).json()

    def upload_to_database(self, db):
        for image in self.images:
            nasa_image = NASAImage(image)
            db.insert_image(nasa_image)

class MySQLConnector:
    def __init__(self, host, username, password, database="apod_database"):
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

class APODDatabase:
    def __init__(self, connector):
        self.connector = connector
        self.create_database()
        self.create_tables()

    def create_database(self):
        query = f"CREATE DATABASE IF NOT EXISTS {self.connector.database};"
        self.connector.execute_query(query)

    def create_tables(self):
        queries = [
            f"USE {self.connector.database};",
            """
            CREATE TABLE IF NOT EXISTS URL (
                date DATE PRIMARY KEY,
                hdurl VARCHAR(128) NOT NULL,
                url VARCHAR(128) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS TITLE (
                date DATE PRIMARY KEY,
                title VARCHAR(128) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS MEDIAINFO (
                date DATE PRIMARY KEY,
                media_type VARCHAR(32) NOT NULL,
                copyright VARCHAR(128) NOT NULL,
                service_version VARCHAR(16) NOT NULL
            );
            """
        ]
        for query in queries:
            self.connector.execute_query(query)
            
        print("Tables created.")

    def insert_image(self, image):
        queries = [
            "INSERT INTO URL VALUES (%s, %s, %s);",
            "INSERT INTO TITLE VALUES (%s, %s);",
            "INSERT INTO MEDIAINFO VALUES (%s, %s, %s, %s);"
        ]
        values = [
            (image.date, image.hdurl, image.url),
            (image.date, image.title),
            (image.date, image.media_type, image.copyright, image.service_version)
        ]
        for i in range(len(queries)):
            query = queries[i]
            value = values[i]
            self.connector.execute_query(query, value)

def main():
    user = "root"
    password = "BearcatGraduate841!"
    DBName = "APOD_Database"

    # Connect to MySQL database
    connector = MySQLConnector("localhost", user, password)
    connector.connect()

    # Load images from NASA's APOD API
    loader = JsonLoader(10)

    # Connect to APOD_Database database
    db = APODDatabase(connector)

    # Upload images to APOD_Database database
    loader.upload_to_database(db)
     
    availableDateQuery = "SELECT * FROM title"
    availableDates = dict(connector.read_query(availableDateQuery))

    print("\nAvailable Dates: ")
    for date in availableDates:
        print(date)

    selected = input("\nSelected Date: ")

    dateObject = datetime.strptime(selected, '%Y-%m-%d').date() # .date truncates unnecessary hours and minutes 
    print(dateObject)

    avilableURLQuery = "SELECT date, url FROM url"
    availableURLs = dict(connector.read_query(avilableURLQuery))

    print("Title: {title} \nURL: {url}".format(title = availableDates[dateObject], url = availableURLs[dateObject]))

    urllib.request.urlretrieve(availableURLs[dateObject], "test.png")

    img = Image.open("test.png")
    img.show()

    # Disconnect from MySQL database
    connector.disconnect()

if __name__ == "__main__":
    main()