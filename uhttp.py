import requests

def http_get(url, par = {}):
    res = requests.get(url, params=par, timeout=5)
    return res