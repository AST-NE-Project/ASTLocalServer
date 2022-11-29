import socket
from time import ctime
import json
import os
import uhttp
import colorama
from colorama import Fore, Style
import time
HOST = '127.0.0.1'
PORT = 3018
ADDR = (HOST, PORT)
BUFFSIZE = 1024
MAX_LISTEN = 1

def MainServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen(MAX_LISTEN)
        while True:
            conn, uaddr = s.accept()
            msg = conn.recv(BUFFSIZE).decode()
            if msg == "exit":
                s.close()
                break
            conn.send("Hello, world!".encode())
            print(conn.recv(BUFFSIZE).decode())
            s.close()
            break

ast_name = Fore.BLUE +  """  ___   _____ _____    _____           _     ______           
 / _ \ /  ___|_   _|  |_   _|         | |    | ___ \          
/ /_\ \\\ `--.  | |      | | ___   ___ | |___ | |_/ / _____  __
|  _  | `--. \ | |      | |/ _ \ / _ \| / __|| ___ \/ _ \ \/ /
| | | |/\__/ / | |      | | (_) | (_) | \__ \| |_/ / (_) >  < 
\_| |_/\____/  \_/      \_/\___/ \___/|_|___/\____/ \___/_/\_\ """ + Fore.RESET
version = "1.0.0"
server_url = 'http://localhost:3000/api/'

def check_updates():
    response = uhttp.http_get(server_url + 'version')
    _version = response.text
    return _version
    

def PrintCopyright():
    colorama.init()
    print(ast_name + '\n')
    v = check_updates()
    if (v != version):
        print(Fore.CYAN + "Currect Version: " + Fore.RED + version + Fore.CYAN +  " != " + Fore.GREEN + v + Fore.CYAN + ", please update.")
        return False
    else:
        print(Fore.CYAN + "Currect Version: " + Fore.GREEN + version + Fore.RESET)
    print('\n')
    return True

if __name__ == '__main__':
    os.system("cls")
    if (PrintCopyright() == False):
        exit()
    
    # check_updates()
    # MainServer()