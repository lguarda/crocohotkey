#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tkinter as tk

from crocohotkey import crocohotkey
from screenlayout import screenlayout


def crocoui(window):
    '''One widget to display them all'''
    bottomframe1 = tk.Frame(window, borderwidth=2, relief=tk.RIDGE)
    bottomframe1.grid(row=1, column=1)
    crocohotkey(bottomframe1)

    bottomframe2 = tk.Frame(window, borderwidth=2, relief=tk.RIDGE)
    bottomframe2.grid(row=1, column=2)
    screenlayout(bottomframe2)


if __name__ == "__main__":

    def close(event):
        window.withdraw()
        sys.exit()

    window = tk.Tk()
    window.bind("<Escape>", close)
    window.title("Config")
    window.attributes("-fullscreen", False)
    window.resizable(False, False)
    crocoui(window)
    sys.exit(window.mainloop())
