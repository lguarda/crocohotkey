#!/usr/bin/env python3
import pynput
import threading
import time

keyboard_sim = pynput.keyboard.Controller()
mouse_sim = pynput.mouse.Controller()

heavy_delay = 0.350

hook_key = 'e'
key_delay = 0.040


def discord():
    global running

    while running:
        mouse_sim.press(pynput.mouse.Button.left)
        time.sleep(key_delay)

        keyboard_sim.press(hook_key)
        time.sleep(key_delay+0.1)
        keyboard_sim.release(hook_key)
        time.sleep(key_delay+0.1)

        mouse_sim.release(pynput.mouse.Button.left)
        time.sleep(key_delay)


def on_press(key):
    global running
    if key == pynput.keyboard.KeyCode.from_char('g'):
        running = True
        t = threading.Thread(target=discord)
        t.start()


def on_release(key):
    global running
    if key == pynput.keyboard.KeyCode.from_char('g'):
        running = False


with pynput.keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
