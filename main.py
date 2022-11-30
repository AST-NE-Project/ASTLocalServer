import socket
from time import ctime
import json
import os
from threading import Thread
import getpass
import psutil
import uhttp
import config
import colorama
from colorama import Fore, Style
import time
HOST = '127.0.0.1'
PORT = 3018
ADDR = (HOST, PORT)
BUFFSIZE = 1024
MAX_LISTEN = 1


ast_name = Fore.BLUE + """  ___   _____ _____    _____           _     ______           
 / _ \ /  ___|_   _|  |_   _|         | |    | ___ \          
/ /_\ \\\ `--.  | |      | | ___   ___ | |___ | |_/ / _____  __
|  _  | `--. \ | |      | |/ _ \ / _ \| / __|| ___ \/ _ \ \/ /
| | | |/\__/ / | |      | | (_) | (_) | \__ \| |_/ / (_) >  < 
\_| |_/\____/  \_/      \_/\___/ \___/|_|___/\____/ \___/_/\_\ """ + Fore.RESET
version = "1.0.0"
server_url = 'http://localhost:3000/api/'
account = ""
token = ""
client_launched = False
ne_launched = False


def check_updates():
    response = uhttp.http_get(server_url + 'version')
    _version = response.text
    return _version


def PrintCopyright():
    colorama.init()
    print(ast_name + '\n')
    v = check_updates()
    if (v != version):
        print(Fore.CYAN + "Currect Version: " + Fore.RED + version +
              Fore.CYAN + " != " + Fore.GREEN + v + Fore.CYAN + ", please update.")
        return False
    else:
        print(Fore.CYAN + "Currect Version: " + Fore.GREEN + version +
              Fore.CYAN + ", no newer version exists." + Fore.RESET)
    print('\n')
    return True


def refr():
    os.system('cls')
    print(ast_name + '\n')


def rendercpu():
    cpu = psutil.cpu_percent()
    if cpu < 50:
        return Fore.GREEN + str(cpu) + "%" + Fore.CYAN
    else:
        return Fore.RED + str(cpu) + "%" + Fore.CYAN


def rendermem():
    cpu = psutil.virtual_memory().percent
    if cpu < 80:
        return Fore.GREEN + str(cpu) + "%" + Fore.CYAN
    else:
        return Fore.RED + str(cpu) + "%" + Fore.CYAN


def renderclient():
    global client_launched
    if client_launched:
        return Fore.GREEN + "LAUNCHED" + Fore.CYAN
    else:
        return Fore.RED + "UNLAUNCHED" + Fore.CYAN


def renderne():
    global ne_launched
    if ne_launched:
        return Fore.GREEN + "LAUNCHED" + Fore.CYAN
    else:
        return Fore.RED + "UNLAUNCHED" + Fore.CYAN


def disp():
    refr()
    print(Fore.CYAN + "CPU Usage: " + rendercpu() + ", MEM Usage: " + rendermem() + ", NE-Launcher: " + renderne() + ", GAME-Client: " + renderclient())

# def ReadyForLaunch():


def MainServer():
    global ne_launched
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen(MAX_LISTEN)
        while True:
            conn, uaddr = s.accept()
            msg = conn.recv(BUFFSIZE).decode()
            if msg == "exit":
                s.close()
                break
            if msg == "launch":
                pass
            if msg == "ne-launch":
                ne_launched = True
                continue
            # conn.send("Hello, world!".encode())
            # print(conn.recv(BUFFSIZE).decode())
            s.close()
            break


def LoginAccount(auto=False):
    # refr()
    global account
    password = ""
    if config.is_section_exist("account") and auto == False:
        account = config.get_config("account", "username")
        password = config.get_config("account", "password")
        auto = True
    while account == "":
        account = input(Fore.WHITE + "Account: " + Fore.RESET)
        refr()
    while password == "":
        password = getpass.getpass(
            Fore.WHITE + "Password [Won't show]: " + Fore.RESET)
        refr()
    res = uhttp.http_get(server_url + 'userlogin',
                         {"username": account, "password": password})
    if res.status_code == 401:
        print(Fore.RED + "Login failed. Check your inputs and try again." + Fore.RESET)
        account = ""
        LoginAccount(auto)
        return
    # print(res.status_code)
    # print(account, password)

    if config.is_section_exist("account") == False:
        config.create_section("account")
    config.set_config("account", "username", account)
    config.set_config("account", "password", password)
    print(Fore.GREEN + "Welcome, " + Fore.CYAN +
          account + Fore.GREEN + "." + Fore.RESET)
    time.sleep(2)


server = Thread(target=MainServer)


def StartLocalServer():
    server.start()
    # server.join(0)


if __name__ == '__main__':
    os.system("cls")
    if (PrintCopyright() == False):
        exit()
    LoginAccount()
    while True:
        disp()
        time.sleep(1)
    # check_updates()
    # MainServer()
