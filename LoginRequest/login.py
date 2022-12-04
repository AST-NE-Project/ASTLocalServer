import requests
import json
import sys


def http_get(url, par={}):
    res = requests.get(url, params=par, timeout=5)
    return res


def LoginAccount(username, password, server = 'http://43.134.185.202:3000/api/'):
    res = http_get(server + 'userlogin',
                   {'username': username, 'password': password})
    if res.status_code == 401:
        print('null')
    else:
        print(json.loads(res.text)['token'])


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print('null')
    else:
        LoginAccount(sys.argv[1], sys.argv[2])
