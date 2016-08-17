#! /usr/bin/env python

import os
import sys
import plistlib
import shutil
import tempfile
import ttk
import tkFileDialog
# My installation of PIL is broken, so I cannot use it.
#import PIL.Image
#import PIL.ImageTk
from Tkinter import *
from subprocess import call
from setuptools import setup

# TCL is not installed in a standard directory, this points it to the correct one
os.environ['TCL_LIBRARY'] = '/usr/local/python/anaconda2/lib/tcl8.5'

class Application(Frame):

	def getinfo(self):
		# Retrieve src
		if not os.path.exists(self.srcEntry.get() + '/Contents'):
			return False

		self.src = self.srcEntry.get()



		# Retrieve data from app info plist
		appInfo = plistlib.readPlist(self.src + '/Contents/info.plist')

		appName = appInfo['CFBundleName']
		appShortVersion = appInfo['CFBundleShortVersionString']
		appLongVersion = appInfo['CFBundleVersion']
		appIconName = appInfo['CFBundleIconFile']



		# Clear entry boxes
		self.nameEntry.delete(0, END)
		self.shortVersionEntry.delete(0, END)
		self.longVersionEntry.delete(0, END)
		self.iconEntry.delete(0, END)

		self.nameEntry.insert(0, appName)
		self.shortVersionEntry.insert(0, appShortVersion)
		self.longVersionEntry.insert(0, appLongVersion)
		self.iconEntry.insert(0, appIconName)

		'''
		# This is code for displaying the app's icon if PIL is not broken
		iconPath = self.src + '/Contents/Resources/' + appIconName
		if not iconPath.endswith('.icns'):
			iconPath += '.icns'
		im = PIL.Image.open(iconPath)
		newim = im.resize((32, 32))

		labelimage = PIL.ImageTk.PhotoImage(newim)
		self.iconPreview.configure(image=labelImage)
		self.iconPreview.image = labelImage
		'''

		self.statusText.set('Gathered info from app')
		self.update_idletasks()
		return True

	def selectSrcFile(self):
		# Clear the input and then get a file from the dialog
		fileoptions = {}
		fileoptions['initialdir'] = os.path.expanduser('~')
		fileoptions['defaultextension'] = '.app'
		fileoptions['filetypes'] = [('apps', '.app'), ('All Files', '.*')]
		fileoptions['title'] = 'Open App'
		self.srcEntry.delete(0, END)
		self.srcEntry.insert(0, tkFileDialog.askopenfilename(**fileoptions))
		self.getinfo()

	def selectDestDir(self):
		# Clear the input and get the destination from the dialog
		diroptions = {}
		diroptions['initialdir'] = os.path.expanduser('~')
		diroptions['mustexist'] = True
		diroptions['title'] = 'Save Destination'
		self.destEntry.delete(0, END)
		self.destEntry.insert(0, tkFileDialog.askdirectory(**diroptions))

	def selectShadowDir(self):
		diroptions = {}
		diroptions['initialdir'] = os.path.expanduser('~')
		diroptions['mustexist'] = True
		diroptions['title'] = 'Shadow Directory'
		self.shadowEntry.delete(0, END)
		self.shadowEntry.insert(0, tkFileDialog.askdirectory(**diroptions))

	def selectPreFile(self):
		fileoptions = {}
		fileoptions['initialdir'] = os.path.expanduser('~')
		fileoptions['title'] = 'Open Executable'
		self.preflightEntry.delete(0, END)
		self.preflightEntry.insert(0, tkFileDialog.askopenfilename(**fileoptions))

	def selectPostFile(self):
		fileoptions = {}
		fileoptions['initialdir'] = os.path.expanduser('~')
		fileoptions['title'] = 'Open Executable'
		self.postflightEntry.delete(0, END)
		self.postflightEntry.insert(0, tkFileDialog.askopenfilename(**fileoptions))

	def clearAll(self):
		self.srcEntry.delete(0, END)
		self.destEntry.delete(0, END)
		self.nameEntry.delete(0, END)
		self.longVersionEntry.delete(0, END)
		self.shortVersionEntry.delete(0, END)
		self.iconEntry.delete(0, END)
		self.shadowEntry.delete(0, END)
		self.preflightEntry.delete(0, END)
		self.postflightEntry.delete(0, END)
		self.statusText.set('Cleared')
		self.update_idletasks()

	def validateInfo(self):
		src = self.srcEntry.get()
		dest = self.destEntry.get()
		name = self.nameEntry.get() + '.app'
		pre = self.preflightEntry.get()
		post = self.postflightEntry.get()

		if not os.path.exists(src) and not src.endswith('.app'):
			self.statusText.set('Invalid Source')
			self.update_idletasks()
			return False
		if not os.path.isdir(dest):
			self.statusText.set('Invalid Destination: Destination does not exist')
			self.update_idletasks()
			return False
		if os.path.exists(os.path.join(dest, name)):
			self.statusText.set('Invalid Destination: App already exists')
			self.update_idletasks()
			return False
		if pre is not '' and not os.path.isfile(pre):
			self.statusText.set('Preflight executable invalid')
			self.update_idletasks()
			return False
		if post is not '' and not os.path.isfile(post):
			self.statusText.set('Postflight executable invalid')
			self.update_idletasks()
			return False
		if self.nameEntry.get() is None:
			self.statusText.set('App must have a name')
			self.update_idletasks()
			return False

		# All good
		return True

	# returns false if app creation fails
	def createApp(self):
		self.statusText.set('Creating App...')
		self.update_idletasks()
		if not self.validateInfo():
			return False


		# Setup variables
		returnValue = True
		launcherScript = os.path.join(DIR, 'appLauncher.py')
		APP = [launcherScript]
		DATA_FILES = []
		OPTIONS = {'argv_emulation': True}

		appName = self.nameEntry.get()
		self.statusText.set('Setting shadow path')
		self.update_idletasks()
		shadowPath = self.shadowEntry.get()
		if not shadowPath:
			shadowPath = '/tmp/' + appName + '.shadow'
		else:
			shadowPath = os.path.join(shadowPath, appName + '.shadow')

		# Custom information for info.plist
		self.statusText.set('Creating info plist')
		self.update_idletasks()
		infoPlist = {'CFBundleShortVersionString': self.shortVersionEntry.get(),
					 'CFBundleVersion': self.longVersionEntry.get(),
					 'CFBundleIdentifier': 'edu.utah.scl.' + appName.lower() + 'wrapper',
					 'ShadowPath': shadowPath,
					 'AppFileName': os.path.basename(os.path.normpath(self.src))}
		OPTIONS['plist'] = infoPlist

		dest = self.destEntry.get()
		OPTIONS['dist_dir'] = dest

		# Create path for icon and append .icns if not already there
		self.statusText.set('Adding Icon')
		self.update_idletasks()
		iconPath = self.iconEntry.get()
		if not os.path.isfile(iconPath):
			iconPath = self.src + '/Contents/Resources/' + iconPath
			if not iconPath.endswith('.icns'):
				iconPath += '.icns'
				if not os.path.isfile(iconPath):
					self.statusText.set('Could not add icon')


		# Verify icon exists and add it to app setup
		if os.path.exists(iconPath):
			OPTIONS['iconfile'] = iconPath


		# make tempory dir for image
		self.statusText.set('Creating tempory directory')
		self.update_idletasks()
		tempDir = tempfile.mkdtemp()
		OPTIONS['bdist_base'] = os.path.join(tempDir, 'build')

		# Add pre/postlight executables if they exists
		self.statusText.set('Checking for pre/postflight executables')
		self.update_idletasks()
		preflightPath = self.preflightEntry.get()
		postflightPath = self.postflightEntry.get()

		if preflightPath:
			if os.path.isfile(preflightPath):
				# copy and rename executable to preflight
				newPath = os.path.join(tempDir, 'preflight')
				preflightPath = shutil.copyfile(preflightPath, newPath)
				OPTIONS['extra_scripts'] = newPath
			else:
				self.statusText.set('Preflight executable is invalid')
				self.update_idletasks()

		if postflightPath:
			if os.path.isfile(postflightPath):
				# copy and rename executable to postflight
				newPath = os.path.join(tempDir, 'postflight')
				shutil.copyfile(postflightPath, newPath)
				# if there is already preflight script, add the postflight with a comma
				if OPTIONS['extra_scripts'] is None:
					OPTIONS['extra_scripts'] = newPath
				else:
					OPTIONS['extra_scripts'] += ', ' + newPath
			else:
				self.statusText.set('Postflight executable is invalid')
				self.update_idletasks()



		# Create app image
		self.statusText.set('Creating disk image... (this may take a while)')
		self.update_idletasks()
		#TODO: create option for setting max image size
		diskImagePath = tempDir + '/' + appName + '.dmg'

		call(['hdiutil', 'create', '-quiet', '-volname', appName, '-srcfolder',  self.src, diskImagePath])

		DATA_FILES.append(diskImagePath)

		# py2app requires special arguments.
		# The semi-standalone flag is being used because it crashes without,
		# however this makes the app rely on the python that is installed on
		# the system.
		self.statusText.set('Backing up environment')
		self.update_idletasks()
		oldArgs = sys.argv
		sys.argv = [oldArgs[0], 'py2app', '--semi-standalone']
		# py2app also screws up the environment, so that needs to backed up
		# restored as well... ugh
		_environ = dict(os.environ)

		# create app
		self.statusText.set('Running py2app')
		self.update_idletasks()
		try:
			setup(
				app=APP,
				name=appName,
				data_files=DATA_FILES,
				options={'py2app': OPTIONS},
				setup_requires=['py2app']
			)
		except TypeError as e:
			self.statusText.set('py2app failed to run properly' + str(e))
			self.update_idletasks()
			returnValue =  False
			#print 'App creation failed: ' + str(e)


		# Clean up temp directory
		self.statusText.set('Cleaning up')
		self.update_idletasks()
		shutil.rmtree(tempDir)
		# restore everything py2app screwed up
		self.statusText.set('Restoring environment')
		self.update_idletasks()
		sys.argv = oldArgs
		os.environ.clear()
		os.environ.update(_environ)
		if returnValue:
			self.statusText.set('App created successfully')

		else:
			self.statusText.set('App could not be created')

		self.update_idletasks()
		return returnValue

	def createWidgets(self):
		self.pack(padx=0, pady=0) # padding for the entire window
		self.configure(background=BG_COLOR)

		labelWidth = 18
		entryWidth = 45

		# Logo
		self.image = PhotoImage(file='logo.ppm', )
		Label(self, bg=BG_COLOR, foreground=FG_COLOR, image=self.image).pack(fill=BOTH, expand=True, padx=0, pady=0)

		# Source and Destination input
		pathFrame = Frame(self)
		pathFrame.configure(background=BG_COLOR)
		pathFrame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=10)

		Label(pathFrame, text='Path to Application:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(pathFrame, text='Path to Launcher:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=1, column=0)

		self.srcEntry = Entry(pathFrame, highlightbackground=BG_COLOR, width=entryWidth-5, validate='focusout', validatecommand=self.getinfo)
		self.destEntry = Entry(pathFrame, highlightbackground=BG_COLOR, width=entryWidth-5)
		self.srcEntry.grid(row=0, column=1)
		self.destEntry.grid(row=1, column=1)

		Button(pathFrame, text='Choose', command=self.selectSrcFile, font='Arial 10', highlightbackground=BG_COLOR, pady=5, padx=2).grid(row=0, column=2)
		Button(pathFrame, text='Choose', command=self.selectDestDir, font='Arial 10', highlightbackground=BG_COLOR, pady=5, padx=2).grid(row=1, column=2)



		ttk.Separator(self, orient=HORIZONTAL).pack(side=TOP, fill=BOTH, padx=5)



		# App info preview and editor
		# Image preview does not work since PIL does not work
		#	self.iconPreview = Label(self, bg=BG_COLOR, foreground=FG_COLOR).pack()

		# Default info plist attributes
		attributeFrame = Frame(self)
		attributeFrame.configure(background=BG_COLOR)
		attributeFrame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=10)


		Label(attributeFrame, text='App Name:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(attributeFrame, text='Long Version Number:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=1, column=0)
		Label(attributeFrame, text='Short Version Number:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=2, column=0)
		Label(attributeFrame, text='Icon File:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=3, column=0)

		self.nameEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.longVersionEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.shortVersionEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.iconEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.nameEntry.grid(row=0, column=1)
		self.longVersionEntry.grid(row=1, column=1)
		self.shortVersionEntry.grid(row=2, column=1)
		self.iconEntry.grid(row=3, column=1)



		ttk.Separator(self, orient=HORIZONTAL).pack(side=TOP, fill=X, pady=5, padx=5)



		# Options
		optionsFrame = Frame(self)
		optionsFrame.configure(background=BG_COLOR)
		optionsFrame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=10)

		Label(optionsFrame, text='Shadow Path:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(optionsFrame, text='Preflight:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=1, column=0)
		Label(optionsFrame, text='Postflight:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=2, column=0)

		self.shadowEntry = Entry(optionsFrame, highlightbackground=BG_COLOR, width=entryWidth-5)
		self.shadowEntry.insert(0, '/tmp')
		self.preflightEntry = Entry(optionsFrame, highlightbackground=BG_COLOR, width=entryWidth-5)
		self.postflightEntry = Entry(optionsFrame, highlightbackground=BG_COLOR, width=entryWidth-5)
		self.shadowEntry.grid(row=0, column=1)
		self.preflightEntry.grid(row=1, column=1)
		self.postflightEntry.grid(row=2, column=1)

		Button(optionsFrame, text='Choose', command=self.selectShadowDir, font='Arial 10', highlightbackground=BG_COLOR, pady=5, padx=2).grid(row=0, column=2)
		Button(optionsFrame, text='Choose', command=self.selectPreFile, font='Arial 10', highlightbackground=BG_COLOR, pady=5, padx=2).grid(row=1, column=2)
		Button(optionsFrame, text='Choose', command=self.selectPostFile, font='Arial 10', highlightbackground=BG_COLOR, pady=5, padx=2).grid(row=2, column=2)


		buttonFrame = Frame(self)
		buttonFrame.configure(background=BG_COLOR)
		buttonFrame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=10)



		self.statusText = StringVar()
		Label(buttonFrame, textvariable=self.statusText, bg=BG_COLOR, font='Arail 10', foreground=FG_COLOR, width=60, padx=5, anchor=W).grid(row=0, column=0)
		Button(buttonFrame, text='Reset', command=self.clearAll, highlightbackground=BG_COLOR, width=8, pady=2).grid(row=0, column=1, padx=2)
		Button(buttonFrame, text='Create', command=self.createApp, highlightbackground=BG_COLOR, width=8, pady=2).grid(row=0, column=2)

	def __init__(self, master=None):
		Frame.__init__(self, master)

		# initialize variables
		self.src = ''
		self.createWidgets()


DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(DIR)
BG_COLOR='lightgrey'
FG_COLOR='black'
root = Tk()
root.configure(background=BG_COLOR)
app=Application(root)
app.mainloop()
