import requests

def http_get(url, par = {}):
    res = requests.get(url, params=par)
    return res