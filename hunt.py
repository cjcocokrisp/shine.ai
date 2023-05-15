import pyautogui
import time

# Define 3DS Controls
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
    pyautogui.keyDown(key)
    pyautogui.keyUp(key)

for x in range(20):
    input_3ds(LEFT)
    time.sleep(0.2)

time.sleep(1)
input_3ds(A)

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