#!/usr/bin/env python3
import pynput
from mouseLongPress import mouseLongPress

delay = 0.350

def on_click(x, y, button, pressed):
    if button == pynput.mouse.Button.button9 and pressed:
        mouseLongPress(pynput.mouse.Button.button9, delay)
    return True

with pynput.mouse.Listener(on_click=on_click) as listener:
    listener.join()
