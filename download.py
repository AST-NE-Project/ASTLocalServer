import requests
import json
import os
import hashlib
import sys
from colorama import Fore, Style, init


def http_get(url, par={}):
    res = requests.get(url, params=par, timeout=5)
    return res


def get_file_list(server_url='http://43.134.185.202:3000/api/'):
    res = http_get(server_url + 'getfilelist')
    return json.loads(res.text)


def get_file(file, size, server_url='http://43.134.185.202:3000/api/'):
    # res = http_get(server_url + 'getlink', {'file': file})
    # if res.status_code != 200:
    #     exit()
    # link = json.loads(res.text)['link']
    link = "https://clor-1301429061.cos.ap-guangzhou.myqcloud.com/ASTResource/" + file
    fsp = file.split('\\')
    # print(fsp)
    path = os.getcwd() + '\\' + '\\'.join(fsp[1:len(fsp) - 1]) + "\\"
    if not os.path.exists(path):
        os.makedirs(path)
    print(Fore.CYAN + 'Download ' + fsp[-1] + '(' + str(size / 1024) + 'KB) from ' + Fore.BLUE + "Tencent COS." + Fore.RESET, end="")
    sys.stdout.flush()
    if (size < 50000):
        res = http_get(link)
        with open(path + fsp[-1], 'wb') as f:
            f.write(res.content)
    else:
        res = requests.get(link, stream=True)
        f = open(path + fsp[-1], 'wb')
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(Fore.GREEN + " Done." + Fore.RESET)
    # download = requests.get()


def check_file(file, md5):
    fsp = file.split('\\')
    path = os.getcwd() + '\\' + '\\'.join(fsp[1:len(fsp) - 1]) + "\\" + fsp[-1]
    # print(md5)
    if (os.path.exists(path) == False):
        return False
    # print(hashlib.md5(open(path, 'rb').read()))
    if (hashlib.md5(open(path, 'rb').read()).hexdigest() == md5):
        return True
    else:
        return False

init()
print(Fore.RED + "补全资源，请不要关闭此窗口！" + Fore.RESET)
if os.path.exists(sys.path[0] + '\\resource\\') == False:
    os.makedirs(sys.path[0] + '\\resource\\')
os.system('cd resource')
os.system("title 补全资源，请不要关闭此窗口！")
sys.path[0] = sys.path[0] + '\\resource\\'

file_list = get_file_list()
for file in file_list:
    # print(file['path'])
    if (check_file(file['path'], file['checksums'])):
        print(file['path'], Fore.CYAN + "Skipped." + Fore.RESET)
        continue
    get_file(file['path'], file['size'])
# fsp = ['a', 'b', 'c']
# path = os.getcwd() + '\\' + '\\'.join(fsp[0:len(fsp) - 1])
# print(path)
