#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import tkinter as tk


def screenlayout(window):
    '''
    Takes in a tk window and append screenlayout widget to it

    This widget will display a Radiobutton list of all script
    location under ~/.screenlayout/ this script can be created
    from arandr
    '''
    scripts_dir = os.getenv("HOME") + "/.screenlayout/"
    screen_layout = [f for f in os.listdir(scripts_dir) if not f.startswith(".")]

    label = tk.Label(window)
    label.config(text="Screen layout")
    label.pack()

    def sel():
        subprocess.run(scripts_dir + screen_layout[var.get()])

    var = tk.IntVar(window, len(screen_layout) + 1)

    for id in range(0, len(screen_layout)):
        text = os.path.splitext(os.path.basename(screen_layout[id]))[0]
        R1 = tk.Radiobutton(window, text=text, variable=var, value=id, command=sel)
        R1.pack()

    none_select = tk.Radiobutton(
        window, text="none", variable=var, value=var.get(), command=sel
    )
    none_select.pack()


if __name__ == "__main__":

    def close(event):
        window.withdraw()
        sys.exit()

    window = tk.Tk()
    window.bind("<Escape>", close)
    window.title("Screen layout")
    window.resizable(False, False)
    screenlayout(window)
    sys.exit(window.mainloop())
