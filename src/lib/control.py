from typing import List
import pyautogui
import time

def input(key: str, cooldown: int, test=None, print_input=None):
    "Used to make inputs on the system, orignally input_3ds()"
    cooldown = int(cooldown)
    pyautogui.keyDown(key)
    pyautogui.keyUp(key)
    if test != None:
        test.update_text(print_input)
        start_time = time.time()
        while time.time() - start_time < cooldown:
            test.update_text(cooldown - int(time.time() - start_time))
            time.sleep(1)
    else: time.sleep(cooldown)

def repeat_button_input(key, sec, interval, test=None, print_input=None):
    """Press a button every second for a certain amount of time (in seconds)."""
    sec = int(sec)
    interval = int(interval)
    start_time = time.time()
    while time.time() - start_time  < sec:
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)
        if test != None:
            test.update_text(f'{print_input} - {int(time.time() - start_time)}')
        time.sleep(interval)

def soft_reset(l, r, start, select, cooldown, test=None):
    cooldown = int(cooldown)
    pyautogui.keyDown(l)
    pyautogui.keyDown(r)
    pyautogui.keyDown(start)
    pyautogui.keyDown(select)
    pyautogui.keyUp(l)
    pyautogui.keyUp(r)
    pyautogui.keyUp(start)
    pyautogui.keyUp(select)

    if test != None:
        test.update_text('Soft Reset')
        start_time = time.time()
        while time.time() - start_time < cooldown:
            test.update_text(cooldown - int(time.time() - start_time))
            time.sleep(1)
    else: time.sleep(cooldown)