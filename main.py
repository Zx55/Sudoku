# -*- coding:utf-8 -*-

try:
    from lib.loop import run

    run()

except ModuleNotFoundError:
    import tkinter as tk
    import tkinter.messagebox as msg

    root = tk.Tk()
    root.withdraw()
    msg.showerror('Error', 'Game files cannot be found.')
