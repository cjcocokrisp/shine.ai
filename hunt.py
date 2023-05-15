import pyautogui
import time

def input_3ds(key: str):
    pyautogui.keyDown(key)
    pyautogui.keyUp(key)

for x in range(20):
    input_3ds('q')
    time.sleep(0.2)

time.sleep(1)
input_3ds('a')

# Controls
# Q - Left
# W - Right
# E - Up
# R - Down
# A - A
# L - S
# R - D
# Start - Z
# Select - X