import pyautogui
import sys
import json


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({'success': False, 'msg': 'account check failed.'}))
        exit()
    account = sys.argv[1]
    password = sys.argv[2]
    path = sys.argv[3] # such as C:\example\
    account_exist = pyautogui.locateCenterOnScreen(path + 'account_exist.png')
    if account_exist is not None:
        pyautogui.click(account_exist)
    
    account_input = pyautogui.locateCenterOnScreen(path + 'account_input.png')
    if account_input is None:
        account_input = pyautogui.locateCenterOnScreen(path + 'account_input2.png')
    if account_input is None:
        print(json.dumps({'success': False, 'msg': 'input field 1 could not find.'}))
        exit()
    pyautogui.click(account_input)
    pyautogui.typewrite(account, interval=0.05)
    pyautogui.press('tab')
    pyautogui.typewrite(password, interval=0.05)

    login = pyautogui.locateCenterOnScreen(path + 'login_button.png')
    if login is None:
        print(json.dumps({'success': False, 'msg': 'login button could not found.'}))
        exit()
    pyautogui.click(login)
