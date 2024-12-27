#!/usr/bin/env python3
import pynput
from keyboardLongPress import keyboardLongPress

delay = 1.350
key='r'

def on_click(x, y, button, pressed):
    #if button == pynput.mouse.Button.button9 and pressed:
    if button == pynput.mouse.Button.left and pressed:
        keyboardLongPress(key, delay)
    return True

with pynput.mouse.Listener(on_click=on_click) as listener:
    listener.join()
