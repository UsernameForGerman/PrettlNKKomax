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
        self.session = Session()
        self.url = '{host}/{db}/{standard}/'.format(
            host=host,
            db=database_name,
            standard=standard,
        )
        self.params = {
            '$format': 'json',
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
            response = self.session.get(self.url + '$metadata', headers=self.headers, params=self.params)
        except ConnectionError:
            return False
        if response.status_code != 200:
            return False
        print('validated')
        self.__validated = True
        return True

    def validated(self):
        return self.__validated

class Request(Connection):

    def __init__(self, username: str, password: str or None, host: str, database_name: str, standard='odata/standard.odata'):
        super().__init__(username, password, host, database_name, standard)
        self.validate()

    def __call__(self, *args, **kwargs):
        if self.validated():
            return True
        else:
            raise AuthenticationError('Not authenticated')

    def get(self, resource, params: dict = None, headers: dict = None):
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        self.headers.update(headers)
        self.params.update(params)
        return self.session.get(
            self.url + resource,
            headers=self.headers,
            params=self.params
        )

    def post(self, resource, data: dict = None, headers: dict = None):
        if data is None:
            data = {}
        if headers is None:
            headers = {}
        return self.session.post(
            self.url + resource,
            headers=self.headers.update(headers),
            data=self.params.update(data)
        )



def get_info(username, password, host, db, standard, resource):
    pass

def get_sells(request: Request, year=None, link=None):
    resource = 'AccumulationRegister_Продажи_RecordType'

    params = {}
    if type(year) is str:
        params['$filter'] = 'year(Period) ge {year}'

    if link is not None:
        resource = link

    # data = {'Количество': 1, 'Сумма': 5000}
    # r = request.post(resource)
    # print(r)
    # print(r.text)
    response = request.get(resource=resource)

    if response.status_code == 200:
        return response.json()

def create_sells(request: Request):
    return

def get_customer():
    pass

def parse_sells(sells):
    pass


if __name__ == '__main__':
    req = Request('web', '1', 'http://192.168.56.101', 'TestBase')
    get_sells(req)
    # print(get_sells(req))
    # print(req.validate())

