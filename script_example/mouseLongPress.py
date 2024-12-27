#!/usr/bin/env python3
import pynput
import time
from threading import Thread, Lock

mutex = Lock()
mouse_sim = pynput.mouse.Controller()

def mouseLongPress(button, delay):
    def run():
        if mutex.acquire(blocking=False):
            mouse_sim.press(pynput.mouse.Button.left)
            time.sleep(delay)
            mouse_sim.release(pynput.mouse.Button.left)
            mutex.release()
    Thread(target=run, args=[]).start()
