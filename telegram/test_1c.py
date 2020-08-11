from requests import Session
from datetime import date as date_class
from base64 import b64encode

base_url = "http://192.168.56.101"
database = 'TestBase'
odata_standard = 'odata/standard.odata'

class AuthenticationError(Exception):
    pass

class Connection:

    def __init__(self, username: str, password: str or None, host: str, database_name: str, standard='odata/standard.odata'):
        self.__session = Session()
        self.url = '{host}/{db}/{standard}/'.format(
            host=host,
            db=database_name,
            standard=standard,
        )
        self.params = {
            '$filter': 'json',
        }

        self.headers = {}
        if password is None:
            self.__credentials = str(
                b64encode('{username}'.format(username=username).encode('ascii'))
            ).split("\'")[1]
        else:
            self.__credentials = str(
                b64encode('{username}:{password}'.format(username=username, password=password).encode('ascii'))
            ).split("\'")[1]
            
        self.headers['Authorization'] = 'Basic {}'.format(self.__credentials)
        self.__validated = False
        
    def validate(self):
        try:
            response = self.__session.get(self.url + '$metadata', headers=self.headers, params=self.params)
        except ConnectionError:
            return False
        if response.status_code != 200:
            return False

        self.__validated = True
        return True

    def get_session(self) -> Session:
        if self.__validated:
            return self.__session
        else:
            self.validate()
            raise AuthenticationError('Login or password is invalid')

class Request(Connection):

    def __init__(self, username: str, password: str or None, host: str, database_name: str, standard='odata/standard.odata'):
        super().__init__(username, password, host, database_name, standard)

    def get(self, resource):
        session = self.get_session()
        return session.get(self.url + resource, headers=self.headers, params=self.params)


def get_info(username, password, host, db, standard, resource):
    pass

def get_sells(connection: Connection, year=None, link=None):
    #
    # req = Request()

    resource = 'AccumulationRegister_Продажи_RecordType'


    if type(year) is str:
        req.params['$filter'] = 'year(Period) ge {year}'

    if type(link) is not None:
        resource = link

    response = req.get(resource)

    if response.status_code == 200:
        return response.json()

def get_customer():
    pass

def parse_sells(sells):
    pass


if __name__ == '__main__':
    connection = Connection('admin', None, base_url, database, odata_standard)

    print(get_sells(connection))

