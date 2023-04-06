import MySQLConnector, JsonLoader, APODDatabase
import os
import configparser
from datetime import datetime
import urllib.request
from PIL import Image

def main():
    dir = os.path.dirname(__file__)
    configFile = os.path.join(dir, 'config.ini')

    config = configparser.ConfigParser()
    config.read(configFile)

    mySQLHost = config['mysql']['host']
    mySQLUser = config['mysql']['username']
    mySQLPass = config['mysql']['password']
    mySQLDB = config['mysql']['database']

    nasaURL = config['nasa']['url']
    nasaAPIKey = config['nasa']['api_key']
    nasaCount = config['nasa']['count']

    # Connect to MySQL database
    connector = MySQLConnector.MySQLConnector(mySQLHost, mySQLUser, mySQLPass, mySQLDB)
    connector.connect()

    # Load images from NASA's APOD API
    loader = JsonLoader.JsonLoader(nasaURL, nasaAPIKey, nasaCount)

    # Connect to APOD_Database database
    db = APODDatabase.APODDatabase(connector)

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