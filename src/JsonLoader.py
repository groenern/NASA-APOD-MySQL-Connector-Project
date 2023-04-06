import NASAImage
import requests

class JsonLoader:
    def __init__(self, url, apiKey, count):
        self.URL_APOD = url
        self.api_key = apiKey
        self.count = count
        self.params = {
            'api_key':self.api_key,
            'count':self.count
        }

        self.images = requests.get(self.URL_APOD,params=self.params).json()

    def upload_to_database(self, db):
        for image in self.images:
            nasa_image = NASAImage.NASAImage(image)
            db.insert_image(nasa_image)