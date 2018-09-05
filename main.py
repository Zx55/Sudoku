# -*- coding:utf-8 -*-

import os
import sys


lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
sys.path.insert(0, lib_dir)

try:
    from loop import run
    run()
    # import soduku
    # soduku.test()

except ModuleNotFoundError:
    import tkinter as tk
    import tkinter.messagebox as msg

    root = tk.Tk()
    root.withdraw()
    msg.showerror('Error', 'Game files cannot be found.')
