#!/usr/bin/env python3
import pynput
import time
from threading import Thread, Lock

mutex = Lock()
keyboard_sim = pynput.keyboard.Controller()

def keyboardLongPress(key, delay):
    def run():
        if mutex.acquire(blocking=False):
            keyboard_sim.press(key)
            time.sleep(delay)
            keyboard_sim.release(key)
            mutex.release()
    Thread(target=run, args=[]).start()
