from datetime import datetime

class NASAImage:
    def __init__(self, image):
        self.date = datetime.strptime(image.get('date', ''), '%Y-%m-%d').date()
        self.hdurl = image.get('hdurl', '')
        self.url = image.get('url', '')
        self.title = image.get('title', '')
        self.media_type = image.get('media_type', '')
        self.copyright = image.get('copyright', '')
        self.service_version = image.get('service_version', '')