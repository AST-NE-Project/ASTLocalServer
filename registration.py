import requests
import sys


def http_get(url, par={}):
    res = requests.get(url, params=par, timeout=5)
    return res


def register_account(account, password, spassword):
    res = http_get('http://api.zshfoj.com/api/register', {'username': account, 'password': password, 'token': spassword})
    if res.status_code != 200:
        print("failed")
    else:
        print("succeeded")


if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print('null')
    else:
        register_account(sys.argv[1], sys.argv[2], sys.argv[3])
