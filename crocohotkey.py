#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import subprocess
import os
import signal
import sys
from pathlib import Path


def close(event):
    event.widget.withdraw()  # if you want to bring it back
    sys.exit()  # if you want to exit the entire thing


def crocohotkey(window):
    UID = os.getuid()
    scripts_dir = os.getenv("HOME") + '/.local/share/crocohotkey'


    scripts = [f for f in os.listdir(scripts_dir) if not f.startswith('.')]
    scripts_status = {}
    scripts_box = {}

    def pid_path(script):
        return (f'/run/user/{UID}/{script}.pid')

    def script_action(script, status):
        if status == 1:
            proc = subprocess.Popen(f"{scripts_dir}/{script}", start_new_session=True)
            with open(pid_path(script), 'w') as f:
                f.write(str(proc.pid))
        else:
            pid_file_name = pid_path(script)
            pid_file = Path(pid_file_name)
            if pid_file.is_file():
                with open(pid_file_name, 'r') as f:
                    pid = f.read()
                    os.kill(int(pid), signal.SIGTERM)
                    os.remove(pid_file_name)

    # this exist only because we can retrive actual check bock pressed whit tkinter
    def build_button_commmand(script):
        def closure():
            script_action(script, scripts_status[script].get())
        return closure

    def callback(sv):
        out = sv.get()
        for script in scripts:
            if script.find(out) != -1:
                scripts_box[script].pack()
            else:
                scripts_box[script].pack_forget()

    sv = tk.StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    e = tk.Entry(window, textvariable=sv)
    e.pack()
    e.focus_set()

    for script in scripts:
        default = 0
        pid_file = Path(pid_path(script))
        if pid_file.is_file():
            default = 1
        scripts_status[script] = tk.IntVar(value=default)
        scripts_box[script] = tk.Checkbutton(window, text=script, variable=scripts_status[script], onvalue=1, offvalue=0, command=build_button_commmand(script))
        scripts_box[script].pack()


if __name__ == '__main__':
    window = tk.Tk()
    window.bind('<Escape>', close)
    window.title('Crocohotkey')
    window.attributes("-fullscreen", False)
    crocohotkey(window)
    sys.exit(window.mainloop())
