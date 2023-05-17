import pyautogui

# Define class that handles 3ds controls
LEFT = 'q'
RIGHT = 'w'
UP = 'e'
DOWN = 'r'
A = 'a'
L = 's'
R = 'd'
START = 'z'
SELECT = 'x'

def input_3ds(key: str):
    "Used to make inputs on the 3DS"
    pyautogui.keyDown(key)
    pyautogui.keyUp(key)

def soft_reset():
    pyautogui.keyDown(L)
    pyautogui.keyDown(R)
    pyautogui.keyDown(START)
    pyautogui.keyDown(SELECT)
    pyautogui.keyUp(L)
    pyautogui.keyUp(R)
    pyautogui.keyUp(START)
    pyautogui.keyUp(SELECT)