from control import encounter, input_3ds, soft_reset, repeat_button_input, A, X, START, LEFT, RIGHT, UP, DOWN 
from PIL import ImageGrab, ImageChops, Image
from pathlib import Path
import tensorflow as tf
import numpy as np
import win32gui
import socket
import time

# Init game soft reset load time and the inputs and intervals and other stuff
load_time = 12
inputs_pre = [START, A, A, LEFT]
intervals_pre = [2.5, 4, 4, 0]
inputs_select = [A, RIGHT, A, A, A, A, DOWN]
intervals_select = [1, 1, 1, 11, 1, 1, 0]
inputs_menu = [X, UP, A, A, A, A, A]
intervals_menu = [0.5, 0.5, 0.5, 0.5, 1, 1, 5]

# Open the neural network
model_name = input("What is the name of the model you are trying to hunt? ")
class_names = ['target_normal', 'target_shiny']
model = tf.keras.models.load_model(model_name)

# Connect to the server and wait to see if bot is connected
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 5000))
s.send(b"SA.h.connect\n")

s.send(b"SA.b.status\n")
while s.recv(2048).decode() != "True":
    print("Waiting for bot to connect...")
    time.sleep(1)
    s.send(b"SA.b.status\n")
print("Connection established beginning hunt")
print("-----------------------------------------------")

#Hunt for the shiny
hunting = True
x = 4
while hunting:
    # Do in game encounter
    soft_reset()
    time.sleep(load_time)
    encounter(inputs_pre, intervals_pre)
    repeat_button_input(A, 26, interval=0.05)
    time.sleep(6)
    encounter(inputs_select, intervals_select)
    repeat_button_input(A, 32, interval=0.05)
    encounter(inputs_menu, intervals_menu)

    # Delay to check for crash
    if x < 8:
        x += 2
    else:
        x = 4

    # Find location of the 3ds window
    winlist = []
    def enum_cb(hwnd, result):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, None)

    for hwnd, title in winlist:
        if title.lower().find('snickerstream') != -1:
            window = (hwnd, title)
            break

    win32gui.SetForegroundWindow(window[0])
    location = win32gui.GetWindowRect(window[0])

    # Check to see if image is on the correct screen
    # UNKNOWN FOR THIS HUNT ATM WILL MOST LIKELY CHANGE

    # Get a screenshot of the 3ds stream
    img = ImageGrab.grab(location)
    width, height = img.size
    img = img.crop(((43, (height / 1.90899) - 1, width - 43, height - 3))) # box for cropping screenshot
    img.save("temp.png", "png")
    img.close()

    # Process with model
    img_path = Path('./temp.png')

    img = tf.keras.utils.load_img(img_path, target_size=(200, 200), keep_aspect_ratio=True)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    predicted_type = class_names[np.argmax(score)]
    print("This encounter most likely is {} with a {:.2f} percent confidence".format(predicted_type, 100 * np.max(score)))

    # Do something based on model output
    if predicted_type == "target_shiny":
        hunting = False
        s.send(b"SA.sh.on_screen\n")
    s.send(b"SA.ss.add\n")

    s.send(b"SA.ss.exists\n")
    while s.recv(2048).decode() != "False":
        print("Bot is handling screenshot...")
        time.sleep(1)
        s.send(b"SA.ss.exists\n")
    print("Bot update complete resuming hunt")
    time.sleep(3)

print("-----------------------------------------------")
s.send(b"SA.e.check\n")
encounters = s.recv(2048).decode()
print(f"The hunt has been completed after {encounters} encounters.")