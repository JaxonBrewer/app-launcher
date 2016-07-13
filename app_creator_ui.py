import os
import sys
import ttk
from Tkinter import *
 

os.environ['TCL_LIBRARY'] = '/usr/local/python/anaconda2/lib/tcl8.5'
class Application(Frame):

	def createWidgets(self):

		self.grid(padx=10, pady=10)
		self.configure(background=background)	
		# src and dest input
		Label(self, text='Path to applicationi:', bg=background).grid(row=0, column=0)
		Label(self, text='New app destination:', bg=background).grid(row=1, column=0)

		self.src = Entry(self, highlightbackground=background)
		self.dest = Entry(self, highlightbackground=background)
		self.src.grid(row=0, column=1, columnspan=2, sticky='ew')
		self.dest.grid(row=1, column=1, columnspan=2, sticky='ew')

		self.s0 = ttk.Separator(self, orient=HORIZONTAL)
		self.s0.grid(row=3, columnspan=3, sticky='ew', padx=3, pady=5)

		# app info preview and editor
		self.image = PhotoImage(file='test.gif')
		Label(self, image=self.image, bg=background).grid(row=4, column=0, rowspan=3)

		Label(self, text='CFBundleName:', bg=background).grid(row=4, column=1)
		Label(self, text='CFBundleShortVersionString:', bg=background).grid(row=5, column=1)
		Label(self, text='CFBundleIconFile:', bg=background).grid(row=6, column=1)

		self.name = Entry(self, highlightbackground=background)
		self.version = Entry(self, highlightbackground=background)
		self.icon = Entry(self, highlightbackground=background)

		self.name.grid(row=4, column=2)
		self.version.grid(row=5, column=2)
		self.icon.grid(row=6, column=2)


		self.s1 = ttk.Separator(self, orient=HORIZONTAL)
		self.s1.grid(row=7, columnspan=3, sticky='ew', padx=3, pady=5)


		# Options
		Label(self, text='Shadow Path:', bg=background).grid(row=8, column=0)
		Label(self, text='Preflight Script:', bg=background).grid(row=9, column=0)
		Label(self, text='Postflight Script:', bg=background).grid(row=10, column=0)

		self.shadow = Entry(self, highlightbackground=background)
		self.preflight = Entry(self, highlightbackground=background)
		self.postflight = Entry(self, highlightbackground=background)

		self.shadow.grid(row=8, column=1, columnspan=2, sticky='ew')
		self.preflight.grid(row=9, column=1, columnspan=2, sticky='ew')
		self.postflight.grid(row=10, column=1, columnspan=2, sticky='ew')

	def __init__(self, master=None):
		Frame.__init__(self, master)
		#self.pack()
		self.createWidgets()

background="lightgrey"

root= Tk()
root.configure(background=background)
app=Application(root)
app.mainloop() 
