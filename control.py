from typing import List
import pyautogui
import time

# Define class that handles 3ds controls
LEFT = 'q'
RIGHT = 'w'
UP = 'e'
DOWN = 'r'
A = 'a'
X = 'f'
L = 's'
R = 'd'
START = 'z'
SELECT = 'x'

def input_3ds(key: str):
    "Used to make inputs on the 3DS"
    pyautogui.keyDown(key)
    pyautogui.keyUp(key)

def encounter(inputs: List[str], intervals: List[int]) -> None:
    """
    Preforms one encounter of the hunt. 
    Inputs is a list of inputs and intervals is the time inbetween each input\n
    
    Example: inputs = [control.A, control.A, control.A], intervals = [5, 5, 5]\n
    This would input A three times with five seconds inbetween
    """
    for i in range(len(inputs)):
        input_3ds(inputs[i])
        time.sleep(intervals[i])

def soft_reset():
    pyautogui.keyDown(L)
    pyautogui.keyDown(R)
    pyautogui.keyDown(START)
    pyautogui.keyDown(SELECT)
    pyautogui.keyUp(L)
    pyautogui.keyUp(R)
    pyautogui.keyUp(START)
    pyautogui.keyUp(SELECT)

def repeat_button_input(key, sec, interval=1):
    """Press a button every second for a certain amount of time (in seconds)."""
    start_time = time.time()
    while time.time() - start_time  < sec:
        input_3ds(key)
        time.sleep(interval)