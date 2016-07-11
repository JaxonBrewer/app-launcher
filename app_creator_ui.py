import os
import sys
from Tkinter import *
from ttk import *
from PIL import Image, ImageTk

root = Tk()

# src and dest input
Label(root, text='Path to application').grid(row=0)
Label(root, text='New app destination').grid(row=1)

src = Entry(root)
dest = Entry(root)

src.grid(row=0, column=1)
dest.grid(row=1, column=1)

s = Separator(root, orient=HORIZONTAL)
s.grid(row=2)

# app info preview and editor
icon = Image.open('test.png')
'''
iconTk = ImageTk.PhotoImage(icon)
preview = Label(image=iconTk)
preview.image = iconTk # keep a reference
preview.grid(row=3)
'''


# Options




root.mainloop()
