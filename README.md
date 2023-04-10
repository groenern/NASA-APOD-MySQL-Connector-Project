# NASA-APOD-MySQL-Connector-Project
This project is a connector that fetches the NASA Astronomy Picture of the Day (APOD) and stores it in a MySQL database. It is built using Python and the NASA APOD API.

## Getting Started
### Prerequisites
- Python 3.x
- MySQL Server and client libraries

### Installation
1. Clone the repository: `git clone https://github.com/groenern/NASA-APOD-MySQL-Connector-Project.git`
2. Install dependencies: `pip install -r requirements.txt`

### Configuration
1. Create a new MySQL Database for the project
2. Open the file called `config.ini`
3. Set the following variables in `config.ini`
   - 'password': [insert your password here]
   - 'database': default to APOD_Database
   - 'api_key': generate api key (https://api.nasa.gov/)
   - 'count': number of images to load (affects performance)
 
 ### Usage
 To run the connector, execute `python main.py` in the project root directory. The connetor will fetch a specified number of APODs (count in config.ini), and populate a MySQL Database with information about each APOD. The user then has the choice to select an image and display it.

## Sample Output
![OutputImage](https://user-images.githubusercontent.com/130081417/230979591-b2f44874-debb-49b6-b59f-3f75f29ae47e.png)
![OutputConsole](https://user-images.githubusercontent.com/130081417/230979631-6d50a76b-1521-484d-ae68-27b2b8bb18aa.png)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
