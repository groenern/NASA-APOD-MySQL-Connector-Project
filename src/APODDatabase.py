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
