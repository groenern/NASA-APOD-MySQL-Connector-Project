 #https://api.nasa.gov/
#https://www.freecodecamp.org/news/connect-python-with-sql/
import requests
import urllib.request
from PIL import Image
from pprint import PrettyPrinter
import mysql.connector

from datetime import datetime

pp = PrettyPrinter()

class JsonLoader:
    URL_APOD = "https://api.nasa.gov/planetary/apod"
    apiKey = 'CD2SnMYuuP4QRtl0BchenBIF1lMFnHwbonpPclNf'
    
    def __init__(self, count):
        self.count = count
        self.params = {
            'api_key':self.apiKey,
            'count':self.count
        }

        self.images = requests.get(self.URL_APOD,params=self.params).json()
        #pp.pprint(self.images)

def createDatabase(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except mysql.connector.Error as error:
        print(f"Error: '{error}'")

def createServerConnection(hostName, userName, userPassword):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostName,
            user = userName,
            passwd = userPassword
        )

        print("MySQL connection successful")
    except mysql.connector.Error as error:
        print(f"Error: '{error}'")

    return connection

def createDatabaseConnection(hostName, userName, userPassword, databaseName):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostName,
            user = userName,
            passwd = userPassword,
            database = databaseName,
            consume_results=True
        )

        print("MySQL Database connection successful")
    except mysql.connector.Error as error:
        print(f"Error: '{error}'")

    return connection

def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print(query + "\nQuery successful")
    except mysql.connector.Error as error:
        print(f"Error: '{error}'")

def readQuery(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print(query + "\nQuery successful")
        return result
    except mysql.connector.Error as error:
        print(f"Error: '{error}'")

myImageLoader = JsonLoader(10) # Load 40 images

# CONNECT TO MYSQL
password = "BearcatGraduate841!"
connection = createServerConnection("localhost", "root", password)

# CREATE DATABASE IN MYSQL
createQuery = "CREATE DATABASE APOD_Database"
createDatabase(connection, createQuery)

# CONNECT TO APOD_DATABASE IN MYSQL
databaseName = "APOD_Database"
databaseConnection = createDatabaseConnection("localhost", "root", password, databaseName)

# CREATE URL TABLE (HDURL + URL)
createURLTable = """
CREATE TABLE URL (
    date DATE PRIMARY KEY,
    hdurl VARCHAR(128) NOT NULL,
    url VARCHAR(128) NOT NULL);
"""

# CREATE DESCRIPTION TABLE (TITLE + EXPLANATION)
createTitleTable = """
CREATE TABLE TITLE (
    date DATE PRIMARY KEY,
    title VARCHAR(128) NOT NULL);
"""

# CREATE MEDIA INFO TABLE (MEDIA_TYPE + COPYRIGHT + SERVICE_VERSION)
createMediaInfoTable = """
CREATE TABLE MEDIAINFO (
    date DATE PRIMARY KEY,
    media_type VARCHAR(32) NOT NULL,
    copyright VARCHAR(128) NOT NULL,
    service_version VARCHAR(16) NOT NULL);
"""

# EXECUTE SQL STATEMENTS FROM ABOVE
executeQuery(databaseConnection, createURLTable)
executeQuery(databaseConnection, createTitleTable)
executeQuery(databaseConnection, createMediaInfoTable)

# POPULATE TABLE VALUE VARIABLES
populateURL = """
INSERT INTO url VALUES
"""

populateTitle = """
INSERT INTO title VALUES
"""

populateMediaInfo = """
INSERT INTO mediainfo VALUES
"""

for thisImage in myImageLoader.images:
    populateURL += "('{date}', '{hdurl}', '{url}'),".format(date = thisImage.get('date'), hdurl = thisImage.get('hdurl'), url = thisImage.get('url'))
    populateTitle += "('{date}', '{title}'),".format(date = thisImage.get('date'), title = thisImage.get('title').replace("'", ""))
    populateMediaInfo += "('{date}', '{mediaType}', '{copyright}', '{serviceVersion}'),".format(date = thisImage.get('date'), mediaType = thisImage.get('media_type'), copyright = thisImage.get('copyright'), serviceVersion = thisImage.get("service_version"))

# TRUNCATES LAST UNNECESSARY LETTER FROM STATEMENT ','
populateURL = populateURL[:-1] 
populateTitle = populateTitle[:-1]
populateMediaInfo = populateMediaInfo[:-1]

# ADD ; TO END SQL STATEMENT
populateURL += ';' 
populateTitle += ';'
populateMediaInfo += ";"

# EXECUTE QUERY TO POPULATE ALL TABLES
executeQuery(databaseConnection, populateURL)
executeQuery(databaseConnection, populateTitle)
executeQuery(databaseConnection, populateMediaInfo)

print("\nDatabase populated\n")

availableDateQuery = "SELECT * FROM title"
availableDates = dict(readQuery(databaseConnection, availableDateQuery))

print("\nAvailable Dates: ")
for date in availableDates:
    print(date)
    
selected = input("\nSelected Date: ")

dateObject = datetime.strptime(selected, '%Y-%m-%d').date() # .date truncates unnecessary hours and minutes 

avilableURLQuery = "SELECT date, url FROM url"
availableURLs = dict(readQuery(databaseConnection, avilableURLQuery))

mediaInfoQuery = "SELECT * FROM mediainfo"
mediaInfo = readQuery(databaseConnection, mediaInfoQuery)

print("Title: {title} \nURL: {url}".format(title = availableDates[dateObject], url = availableURLs[dateObject]))

for mInfo in mediaInfo:
    if mInfo[0] == dateObject:
        print("Media type: {media} \nCopyright: {copyright} \nVersion: {version}".format(media = mInfo[1], copyright = mInfo[2], version = mInfo[3]))

urllib.request.urlretrieve(availableURLs[dateObject], "test.png")

img = Image.open("test.png")
img.show()