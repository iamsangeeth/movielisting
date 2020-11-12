import requests, os
from base64 import b64encode

def get_movieslist(page):

    url = "https://demo.credy.in/api/v1/maya/movies/"
    if page:
        url = url + "?page=" + page

    #retry logic

    MAX_TRIES = 3
    tries = 0
    resp = None
    while True:
        response = requests.get(url, auth=(os.environ['username'], os.environ['password']))
        if response.status_code !=200:
            if tries < MAX_TRIES:
                tries += 1
                continue
            else:
                return []
        else:
            break

    #data parsing and next and previous fixings

    data = response.json()
    if data['next']:
        if page:
            data['next'] = "http://localhost:8000/movies/?page=" + str(int(page)+1)
        else:
            data['next'] = "http://localhost:8000/movies/?page=1"
    if data['previous']:
        if page and int(page)-1>0:
            data['previous'] = "http://localhost:8000/movies/?page=" + str(int(page)-1)
    return data