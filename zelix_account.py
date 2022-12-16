import config
import uhttp
import hashlib
import time


account = config.get_config('zelix', 'username')
password = config.get_config('zelix', 'password')
hwid = config.get_config('zelix', 'hwid')

timestamp = str(int(time.time()))
sign = hashlib.md5(str(account + password + timestamp).encode()).hexdigest()[8:24]

res = uhttp.http_get("http://121.62.61.198:82/getaccount?account="+ account + "&timestamp=" + timestamp + "&sign=" + sign)
print(res.text)
