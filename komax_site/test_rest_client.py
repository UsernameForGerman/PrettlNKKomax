import requests, json

session = requests.session()

username = 'operator1'
password = 'prettl-operator'
BASE_URL = 'http://localhost:8000/'


request = session.post(BASE_URL + 'api/v1/auth/', data={
    'username': username,
    'password': password,
})

result = request.json()

token = result.get('token', None)

session.headers = {
    'Authorization': 'Token {}'.format(token)
}
request = session.get(BASE_URL + 'api/v2/komax_tasks/')

result = request.json()

print(result)

