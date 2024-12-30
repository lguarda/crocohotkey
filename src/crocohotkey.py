#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import signal
import subprocess
import sys
import tkinter as tk
from pathlib import Path

def fuzzy_match(string, into):
    string = string.lower()
    into = into.lower()

    for char in string:
        offset = into.find(char)
        if offset < 0:
            return False
        into = into[offset:]
    return True

def crocohotkey(window):
    """
    Take in a tk window and append crocohotkey widget to it

    This widget will display the list of all available script with check box
    so you will be able to toggle on and of the script.
    It's also contain a search bar so you can quickly find a script.
    """
    UID = os.getuid()
    scripts_dir = os.getenv("HOME") + "/.local/share/crocohotkey"
    regex = r"croco(.*)\.py"
    scripts = [f for f in os.listdir(scripts_dir) if f.startswith("croco")]
    scripts = list(map(lambda f: re.sub(regex, "\\1", f, 0), scripts))
    scripts_status = {}
    scripts_box = {}

    def pid_path(script):
        return f"/run/user/{UID}/{script}.pid"

    def script_action(script, status):
        if status == 1:
            proc = subprocess.Popen(f"{scripts_dir}/{script}", start_new_session=True)
            with open(pid_path(script), "w") as f:
                f.write(str(proc.pid))
        else:
            pid_file_name = pid_path(script)
            pid_file = Path(pid_file_name)
            if pid_file.is_file():
                with open(pid_file_name, "r") as f:
                    pid = f.read()
                    os.kill(int(pid), signal.SIGTERM)
                    os.remove(pid_file_name)

    # this exist only because we can retrieve actual check bock pressed whit tkinter
    def build_button_commmand(script):
        def closure():
            script_action(script, scripts_status[script].get())

        return closure

    def callback(search_text):
        input = search_text.get()
        for script in scripts:
            if fuzzy_match(input, script):
                scripts_box[script].pack()
            else:
                scripts_box[script].pack_forget()

    search_text = tk.StringVar()
    search_text.trace(
        "w", lambda name, index, mode, search_text=search_text: callback(search_text)
    )
    e = tk.Entry(window, textvariable=search_text)
    e.pack()
    e.focus_set()

    for script in scripts:
        default = 0
        pid_file = Path(pid_path(script))
        if pid_file.is_file():
            default = 1
        scripts_status[script] = tk.IntVar(value=default)
        scripts_box[script] = tk.Checkbutton(
            window,
            text=script,
            variable=scripts_status[script],
            onvalue=1,
            offvalue=0,
            command=build_button_commmand(script),
        )
        scripts_box[script].pack()


if __name__ == "__main__":

    def close(event):
        event.widget.withdraw()
        sys.exit()

    window = tk.Tk()
    window.bind("<Escape>", close)
    window.title("Crocohotkey")
    window.attributes("-fullscreen", False)
    crocohotkey(window)
    sys.exit(window.mainloop())
