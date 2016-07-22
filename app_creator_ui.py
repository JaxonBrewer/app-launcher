import os
import sys
import plistlib
import shutil
import tempfile
import ttk
#import tkFileDialog
from Tkinter import *
from subprocess import call
from setuptools import setup

# TCL is not installed in a standard directory, this points it to the correct one
os.environ['TCL_LIBRARY'] = '/usr/local/python/anaconda2/lib/tcl8.5'

class Application(Frame):

	def getinfo(self):
		# Retrieve src
		self.src = self.srcEntry.get()

		#TODO: make sure paths are valid.


		# Retrieve data from app info plist
		appInfo = plistlib.readPlist(source + '/Contents/info.plist')

		appName = appInfo['CFBundleName']
		appVersion = appInfo['CFBundleShortVersionString']
		appIconName = appInfo['CFBundleIconFile']

		self.nameEntry.insert(0, appName)
		self.versionEntry.insert(0, appVersion)
		self.iconEntry.insert(0, appIconName)




	def createApp(self):
		# Setup variables
		APP = ['appLauncher.py']
		DATA_FILES = []
		OPTIONS = {'argv_emulation': True}

		# Custom information for info.plist
		print 'Creating info.plist'
		infoPlist = {'CFBundleShortVersionString': self.versionEntry.get(),
					 'CFBundleIdentifier': 'edu.utah.scl.' + self.nameEntry.get().lower() + 'wrapper'}
		OPTIONS['plist'] = infoPlist

		dest = self.destEntry.get()
		if not os.path.exists(dest):
			# destination Invalid
			exit()
		OPTIONS['dest_dir'] = dest

		# Create path for icon and append .icns if not already there
		iconPath = self.src + '/Contents/Resources/' + self.iconEntry.get()
		if not iconPath.endswith('.icns'):
			iconPath += '.icns'
		# Verify icon exists and add it to app setup
		if os.path.exists(iconPath):
			OPTIONS['iconfile'] = iconPath

		# make tempory dir for image
		tempDir = tempfile.mkdtemp()

		# Create app image
		#TODO: create option for setting max image size
		imagePath = tempDir + '/' + self.nameEntry.get() + '.dmg'
		call(['hdiutil', 'create', '-srcfolder',  self.src, imagePath])

		DATA_FILES.append(imagePath)

		# py2app requires special arguments
		oldArgs = sys.argv
		sys.argv = [oldArgs[0], 'py2app', '--semi-standalone']

		# create app
		#print 'Creating App'
		try:
			setup(
				app=APP,
				name=self.nameEntry.get(),
				data_files=DATA_FILES,
				options={'py2app': OPTIONS},
				setup_requires=['py2app']
			)
		except TypeError as e:
			print 'App creation failed: ' + str(e)

		# Clean up temp directory
		print 'Cleaning up'
		shutil.rmtree(tempDir)
		sys.argv = oldArgs # restore the old arguments

	def createWidgets(self):
		self.pack(padx=10, pady=10) # padding for the entire window
		self.configure(background=BG_COLOR)

		labelWidth = 16
		entryWidth = 24
		# Source and Destination input
		pathFrame = Frame(self)
		pathFrame.configure(background=BG_COLOR)
		pathFrame.pack(side=TOP, fill=BOTH, expand=True)

		Label(pathFrame, text='Path to Application:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(pathFrame, text='Path to Launcher:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=1, column=0)

		self.srcEntry = Entry(pathFrame, highlightbackground=BG_COLOR, width=entryWidth).grid(row=0, column=1)
		self.destEntry = Entry(pathFrame, highlightbackground=BG_COLOR, width=entryWidth).grid(row=1, column=1)



		self.s0 = ttk.Separator(self, orient=HORIZONTAL)
		self.s0.pack(side=TOP, fill=BOTH, pady=5)



		# App info preview and editor
		self.image = PhotoImage(file='test.gif') #TODO: replace the preview image
		Label(self, image=self.image, bg=BG_COLOR).pack()

		# Default info plist attributes
		attributeFrame = Frame(self)
		attributeFrame.configure(background=BG_COLOR)
		attributeFrame.pack(side=TOP, fill=BOTH, expand=True)


		Label(attributeFrame, text='App Name:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(attributeFrame, text='(CFBundleName)', bg=BG_COLOR, font='Arial 10', anchor=E).grid(row=1, column=0, sticky=E)
		Label(attributeFrame, text='Version Number:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=2, column=0)
		Label(attributeFrame, text='(CFBundleShortVersionString)', bg=BG_COLOR, font="Arial 10", anchor=E).grid(row=3, column=0, sticky=E)
		Label(attributeFrame, text='Icon File:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=4, column=0)
		Label(attributeFrame, text='(CFBundleIconFile)', bg=BG_COLOR, font="Arial 10", anchor=E).grid(row=5, column=0, sticky=E)

		self.nameEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.versionEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.iconEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)

		self.nameEntry.grid(row=0, rowspan=2, column=1)
		self.versionEntry.grid(row=2, rowspan=2, column=1)
		self.iconEntry.grid(row=4, rowspan=2, column=1)


		self.s1 = ttk.Separator(self, orient=HORIZONTAL)
		self.s1.pack(side=TOP, fill=X, pady=5)


		# Options
		optionsFrame = Frame(self)
		optionsFrame.configure(background=BG_COLOR)
		optionsFrame.pack(side=TOP, fill=BOTH, expand=True)

		Label(optionsFrame, text='Shadow Path:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(optionsFrame, text='Preflight Script:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=1, column=0)
		Label(optionsFrame, text='Postflight Script:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=2, column=0)

		self.shadowEntry = Entry(optionsFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.preflightEntry = Entry(optionsFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.postflightEntry = Entry(optionsFrame, highlightbackground=BG_COLOR, width=entryWidth)

		self.shadowEntry.grid(row=0, column=1)
		self.preflightEntry.grid(row=1, column=1)
		self.postflightEntry.grid(row=2, column=1)

		Button(self, text="Create", command=self.createApp, width=20, pady=5, highlightbackground=BG_COLOR).pack()

	def __init__(self, master=None):
		Frame.__init__(self, master)

		# initialize variables
		self.src = ''

		self.createWidgets()

BG_COLOR="lightgrey"

root= Tk()
root.configure(background=BG_COLOR)
app=Application(root)
app.mainloop()
