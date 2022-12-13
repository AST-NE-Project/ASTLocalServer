import requests
import json
import os
import hashlib
import asyncio
import sys
from colorama import Fore, Style, init

import asyncio
from aiohttp import ClientSession


tasks = []
async def http_get_file(url, path, semaphore):
    async with semaphore:
        async with ClientSession() as session:
            async with session.get(url) as response:
                response = await response.read()
                # print (path)
                with open(path, 'wb') as f:
                    # print (path)
                    f.write(response)
                    print(Fore.GREEN + "Downloaded " + Fore.CYAN + path.split('\\')[-1] + "." + Fore.RESET)
                


loop = asyncio.get_event_loop()


def http_get(url, par={}):
    res = requests.get(url, params=par, timeout=5)
    return res


def get_file_list(server_url='http://api.zshfoj.com/api/'):
    res = http_get(server_url + 'getfilelist')
    # print(res.text)
    return json.loads(res.text)

tasks = []

def get_file(file, size, server_url='http://api.zshfoj.com/api/'):
    global semaphore
    link = "http://api.zshfoj.com/api/getfile?path=" + file.replace('\\', '/')
    fsp = file.split('\\')
    # print(fsp)
    path = os.getcwd() + '\\' + '\\'.join(fsp[0:len(fsp) - 1]) + "\\"
    if not os.path.exists(path):
        os.makedirs(path)
    print(Fore.CYAN + 'Download ' + fsp[-1] + '(' + str(size / 1024) + 'KB) from ' + Fore.BLUE + "Tencent COS." + Fore.RESET, end="")
    sys.stdout.flush()
    task = asyncio.ensure_future(http_get_file(link, path + fsp[-1], semaphore))
    tasks.append(task)
    print(Fore.GREEN + " Added." + Fore.RESET)
    # download = requests.get()


def check_file(file, md5):
    fsp = file.split('\\')
    path = os.getcwd() + '\\' + '\\'.join(fsp[0:len(fsp) - 1]) + "\\" + fsp[-1]
    # print(path)
    if (os.path.exists(path) == False):
        return False
    # print(hashlib.md5(open(path, 'rb').read()).hexdigest(), md5)
    if (hashlib.md5(open(path, 'rb').read()).hexdigest() == md5):
        return True
    else:
        return False

init()
print(Fore.RED + "补全资源，请不要关闭此窗口！" + Fore.RESET)
os.system("title 补全资源，请不要关闭此窗口！")
# check_file("clientLauncher\\assets\\indexes\\1.12.json", "0")

file_list = get_file_list()
loop = asyncio.get_event_loop()
semaphore = asyncio.Semaphore(64)
for file in file_list:
    if (check_file(file['path'], file['checksums'])):
        print(file['path'], Fore.CYAN + "Skipped." + Fore.RESET)
        continue
    get_file(file['path'], file['size'])
    # print("add")
    # print(check_file(file['path'], file['checksums']))
    # break
loop.run_until_complete(asyncio.wait(tasks))
# fsp = ['a', 'b', 'c']
# path = os.getcwd() + '\\' + '\\'.join(fsp[0:len(fsp) - 1])
# print(path)
