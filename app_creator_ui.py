import os
import sys
import plistlib
import shutil
import tempfile
import ttk
from Tkinter import *
from subprocess import call
from setuptools import setup
 

os.environ['TCL_LIBRARY'] = '/usr/local/python/anaconda2/lib/tcl8.5'
class Application(Frame):
	def createApp(caller):	
		# Setup variables
		APP = ['appLauncher.py']
		DATA_FILES = []
		OPTIONS = {'argv_emulation': True}

		source = caller.src.get()
		dest = caller.src.get()

		# Open App's info.plist so information can be extracted
		print 'Getting app info'
		appInfo = plistlib.readPlist(source + '/Contents/info.plist')

		self.appName = appInfo['CFBundleName']	
		self.appVersion = appInfo['CFBundleShortVersionString']
		self.appIconName = appInfo['CFBundleIconFile']

		# Custom information for info.plist
		print 'Creating info.plist'
		infoPlist = {'CFBundleShortVersionString': self.appVersion,
					 'CFBundleIdentifier': 'edu.utah.scl.' + self.appName.lower() + 'wrapper'}
		OPTIONS['plist'] = infoPlist

		# Append .icns to icon name from info.plist if not already there
		print 'Fetching app icon'
		if not self.appIconName.endswith('.icns'):
			self.appIconName += '.icns'
		iconPath = source + '/Contents/Resources/' + self.appIconName

		# Verify icon exists and add it to app setup
		if os.path.exists(iconPath):
			OPTIONS['iconfile'] = iconPath

		# Check that destination is valid and add it to app setup
		if not os.path.exists(destPath):
			print 'Invalid Destination!'
			exit()
		OPTIONS['dist_dir'] = destPath	

		# make tempory dir for image
		tempDir = tempfile.mkdtemp()

		# Create app image
		print 'Creating App image'
		imagePath = tempDir + '/' + self.appName + '.dmg'
		call(['hdiutil', 'create', '-srcfolder',  source, imagePath])
		
		DATA_FILES.append(imagePath)

		# create app
		print 'Creating App'
		try:
			setup(
				app=APP,
				name=self.appName,
				data_files=DATA_FILES,
				options={'py2app': OPTIONS},
				setup_requires=['py2app']
			)
		except TypeError as e:
			print 'App creation failed: ' + str(e)
			
		# Clean up temp directory
		print 'Cleaning up'
		shutil.rmtree(tempDir)
			
		print 'Done'

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

		self.name = Entry(self,textvariable=self.appName, highlightbackground=background)
		self.version = Entry(self, textvariable=self.appName, highlightbackground=background)
		self.icon = Entry(self, textvariable=self.appIconName, highlightbackground=background)

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

		Button(self, text="Create", command=self.createApp, width=20, pady=5, highlightbackground=background).grid(row=11, column=2)

	def __init__(self, master=None):
		Frame.__init__(self, master)
		#self.pack()

		self.appName = ""
		self.appVersion = ""
		self.appIconName = ""

		self.createWidgets()
	
background="lightgrey"

root= Tk()
root.configure(background=background)
app=Application(root)
app.mainloop() 
