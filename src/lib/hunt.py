from importlib.machinery import SourceFileLoader
from src.lib.gen_cmd_script import gen_cmd_script
from src.lib.screenshot import take_screenshot
from pathlib import Path
import tensorflow as tf
import numpy as np
import socket
import time
import os

def run_hunt(file, settings, exit_event, gui):
    path = gen_cmd_script(file)
    script = SourceFileLoader('encounter', path).load_module()
    
    path = file.path
    while path.find('/') != -1:
        path = path[path.find('/') + 1:]
    path = path[:path.find('.')]

    if os.path.isfile(f'data/{path}/crash.png'):
        crash_detection_enabled = True
    else: crash_detection_enabled = False

    class_names = ['target_normal', 'target_shiny']
    model = tf.keras.models.load_model(f'data/{path}/model')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5000))
    s.send(b'SA.h.connect\n')
    s.send(b"SA.b.status\n")
    while s.recv(2048).decode() != "True":
        print('Waiting for bot to connect...')
        time.sleep(1)
        s.send(b"SA.b.status\n")
        # Thread kill
        if exit_event.is_set():
            return

    path = path.replace('encounter.py', '')
    hunting = True
    while hunting:
        # Thread kill
        if exit_event.is_set():
            return

        script.encounter(settings, None)
        crashed = take_screenshot(
                        path, settings,
                        int(settings.hunt['custom_x']), 
                        int(settings.hunt['custom_y']),
                        int(settings.hunt['custom_width']),
                        int(settings.hunt['custom_height']),
                        crash_check=crash_detection_enabled
                       )
        if crashed:
            gui.handle_crash()

        img_path = Path(f'data/{path}/current.png')
        img = tf.keras.utils.load_img(img_path, target_size=(200, 200), keep_aspect_ratio=True)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        predicted_type = class_names[np.argmax(score)]

        if predicted_type == "target_shiny":
            hunting = False
            s.send(b"SA.sh.on_screen\n")
        s.send(b"SA.ss.add\n")

        s.send(b"SA.ss.exists\n")
        while s.recv(2048).decode() != "False":
            time.sleep(1)
            s.send(b"SA.ss.exists\n")
        time.sleep(3)
    gui.shiny_found()
    while True:
        if exit_event.is_set():
            break