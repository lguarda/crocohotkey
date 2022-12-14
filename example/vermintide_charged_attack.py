#!/usr/bin/env python3
import pynput
import time

mouse_sim = pynput.mouse.Controller()

heavy_delay = 0.350


def discord():
    mouse_sim.press(pynput.mouse.Button.left)
    time.sleep(heavy_delay)
    mouse_sim.release(pynput.mouse.Button.left)

def on_click(x, y, button, pressed):
    if button == pynput.mouse.Button.button9 and pressed:
        discord()
    return True

with pynput.mouse.Listener(on_click=on_click) as listener:
    listener.join()
