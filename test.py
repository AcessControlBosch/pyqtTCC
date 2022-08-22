import requests

def getData():
    url = requests.get('http://localhost:8000/users/460161').json()
    print(url)
    json_response = dict(url)
    print(type(json_response))
    print(json_response['name'])


getData()