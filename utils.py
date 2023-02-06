import requests
from pprint import pprint


def get_data(url):
    try:
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:             # OK
            return response.json(), "INFO: Data received successfully"
    except requests.exceptions.ConnectionError:   # connection error
        return None, "ERROR requests.exceptions.ConnectionError"
    except requests.exceptions.JSONDecodeError:   # format error
#        print(response.url)
        return None, "ERROR requests.exceptions.JSONDecodeError"

