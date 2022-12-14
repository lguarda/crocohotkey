#!/usr/bin/env python3
import pynput
import time

keyboard_sim = pynput.keyboard.Controller()
mouse_sim = pynput.mouse.Controller()

key_delay = 0.040
rod_key = '`'
mirror_key = '9'
weapon_key = '1'

def discord():
    keyboard_sim.press(rod_key)
    time.sleep(key_delay)
    keyboard_sim.release(rod_key)
    time.sleep(key_delay)
    mouse_sim.press(pynput.mouse.Button.left)
    time.sleep(key_delay)
    mouse_sim.release(pynput.mouse.Button.left)
    time.sleep(key_delay)
    keyboard_sim.press(weapon_key)
    time.sleep(key_delay)
    keyboard_sim.release(weapon_key)

def mirror():
    keyboard_sim.press(mirror_key)
    time.sleep(key_delay)
    keyboard_sim.release(mirror_key)
    time.sleep(key_delay)
    mouse_sim.press(pynput.mouse.Button.left)
    time.sleep(key_delay)
    mouse_sim.release(pynput.mouse.Button.left)
    time.sleep(key_delay)
    keyboard_sim.press(weapon_key)
    time.sleep(key_delay)
    keyboard_sim.release(weapon_key)

def on_click(x, y, button, pressed):
    if button == pynput.mouse.Button.button9 and pressed:
        discord()
    elif button == pynput.mouse.Button.middle and pressed:
        mirror()
    return True

with pynput.mouse.Listener(on_click=on_click) as listener:
    listener.join()
