import socket
import json
import os
from threading import Thread
import getpass
import inspect
import ctypes
# import threading
import psutil
import win32gui
import keyboard
import uhttp
import config
import colorama
from colorama import Fore, Style
import time
import win32process
import sys

HOST = '127.0.0.1'
PORT = 3018
ADDR = (HOST, PORT)
BUFFSIZE = 1024
MAX_LISTEN = 1
__DEBUG_MODE__ = 0


ast_name = Fore.BLUE + """  ___   _____ _____    _____           _     ______           
 / _ \ /  ___|_   _|  |_   _|         | |    | ___ \          
/ /_\ \\\ `--.  | |      | | ___   ___ | |___ | |_/ / _____  __
|  _  | `--. \ | |      | |/ _ \ / _ \| / __|| ___ \/ _ \ \/ /
| | | |/\__/ / | |      | | (_) | (_) | \__ \| |_/ / (_) >  < 
\_| |_/\____/  \_/      \_/\___/ \___/|_|___/\____/ \___/_/\_\ """ + Fore.RESET
version = "1.0.0"
if __DEBUG_MODE__:
    server_url = 'http://127.0.0.1:3000/api/'
else:
    server_url = 'http://43.134.185.202:3000/api/'
account = ""
token = ""
client_launched = False
ne_launched = False
extra_info = ""
chat_mode = False
msg_records = ""
last_message = 0


def clear():
    os.system('cls')


def refr():
    clear()
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
    global extra_info, chat_mode
    if chat_mode == False:
        refr()
        print(Fore.CYAN + "CPU Usage: " + rendercpu() + ", MEM Usage: " + rendermem() +
              ", NE-Launcher: " + renderne() + ", GAME-Client: " + renderclient() + '.')
        if extra_info != "":
            print('\n' + extra_info)
        print('\n')
        print(Fore.CYAN + "Press" + Fore.YELLOW +
              " [Key C]" + Fore.CYAN + " to chat with AST users, press " + Fore.YELLOW + "[Key S]" + Fore.CYAN + " to stop AST.")
        print(msg_records)


def check_updates():
    response = uhttp.http_get(server_url + 'version')
    _version = response.text
    return _version


def LaunchClientTips(left=5):
    global extra_info, client_launched
    if left == -1:
        extra_info = ""
        disp()
        return
    if left == 0:
        extra_info = Fore.YELLOW + "Game Launched!" + Fore.RESET
        client_launched = True
        disp()
        time.sleep(2)
        LaunchClientTips(-1)
        return
    extra_info = "Client will launch in " + Fore.GREEN + \
        str(left) + Fore.CYAN + " seconds." + Fore.RESET
    disp()
    time.sleep(1)
    LaunchClientTips(left - 1)


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

# def ReadyForLaunch():


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def MainServer():
    global ne_launched, s
    with s:
        s.bind(ADDR)
        s.listen(MAX_LISTEN)
        while True:
            conn, uaddr = s.accept()
            msg = conn.recv(BUFFSIZE).decode()
            if msg == "exit":
                s.close()
                break
            if msg == "game_launch":
                thTips = Thread(target=LaunchClientTips())
                thTips.start()
                continue
            # conn.send("Hello, world!".encode())
            # print(conn.recv(BUFFSIZE).decode())
        s.close()


def LoginAccount(auto=False):
    # refr()
    global account, token
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
    # print()
    # print(account, password)
    token = json.loads(res.text)['token']
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


def ChatMode():
    global chat_mode, account, token
    while True:
        keyboard.wait('c')
        tid, pid = win32process.GetWindowThreadProcessId(
            win32gui.GetForegroundWindow())
        print(pid, os.getppid(), os.getpid())
        if (pid == os.getpid() or pid == os.getppid()):
            chat_mode = True
            refr()
            sys.stdin.flush()
            mess = input(Fore.MAGENTA + "[Input Message]: " + Fore.RESET)
            res = uhttp.http_get(server_url + 'sendmessage',
                                 {'username': account, 'message': mess, 'token': token})
            if res.status_code != 200:
                print(Fore.RED + "Failed to send message!")
            chat_mode = False
            disp()


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def GetMessage():
    global token, last_message, msg_records
    # print ("Try 2 get!")
    res = uhttp.http_get(server_url + "getmessage",
                         {'token': token, 'since': last_message})
    if res.status_code != 200:
        print(Fore.RED + "Errors happened when get message: " +
              json.loads(res.text)['msg'])
        return
    msg = json.loads(res.text)['records']
    for m in msg:
        if m['level'] == 1:
            msg_records = msg_records + Fore.CYAN + \
                '[USER] ' + Fore.RESET + m['username'] + ': '
        elif m['level'] == 10:
            msg_records = msg_records + Fore.GREEN + \
                '[ADMIN] ' + Fore.YELLOW + m['username'] + Fore.RESET + ': '
        msg_records = msg_records + m['message'] + '\n'
    # print("GET:", len(msg))
    lines = msg_records.split('\n')
    if len(lines) > 10:
        msg_records = Fore.RESET
        for i in range(len(lines) - 10, len(lines)):
            if lines[i] == "":
                continue    
            msg_records = msg_records + lines[i] + '\n'
    if len(msg) != 0:
        last_message = msg[-1]['time']
        disp()
        # print(lines)


def MessageGetter():
    global token, last_message, msg_records
    msg_records = Fore.RESET
    while True:
        # print("start to get.")
        GetMessage()
        time.sleep(1)


if __name__ == '__main__':
    clear()
    colorama.init()
    if (PrintCopyright() == False):
        exit()
    LoginAccount()
    # GetMessage()
    msgg = Thread(target=MessageGetter)
    msgg.start()
    server.start()
    chat = Thread(target=ChatMode)
    chat.start()
    disp()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # print("key board stop!")
        stop_thread(chat)
        stop_thread(msgg)
        print('stop!')
        s.close()
        # stop_thread(server)
    # check_updates()
    # MainServer()
