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

		return True

	def openFile(self):
		# Clear the input and then get a file from the dialog
		self.srcEntry.delete(0, END)
		self.srcEntry.insert(0, tkFileDialog.askopenfilename(**self.file_opt))
		self.getinfo()

	def openDir(self):
		# Clear the input and get the destination from the dialog
		self.destEntry.delete(0, END)
		self.destEntry.insert(0, tkFileDialog.askdirectory(**self.dir_opt))

	# returns false if app creation fails
	def createApp(self):
		# Setup variables
		APP = ['appLauncher.py']
		DATA_FILES = []
		OPTIONS = {'argv_emulation': True}

		appName = self.nameEntry.get()
		shadowPath = self.shadowEntry.get()
		if not shadowPath:
			shadowPath = '/tmp/' + appName + '.shadow'
		else:
			shadowPath = os.path.join(shadowPath, appName + '.shadow')

		# Custom information for info.plist
		infoPlist = {'CFBundleShortVersionString': self.shortVersionEntry.get(),
					 'CFBundleVersion': self.longVersionEntry.get(),
					 'CFBundleIdentifier': 'edu.utah.scl.' + appName.lower() + 'wrapper',
					 'ShadowPath': shadowPath}
		OPTIONS['plist'] = infoPlist

		dest = self.destEntry.get()
		if not os.path.exists(dest):
			# destination Invalid
			return False
		OPTIONS['dist_dir'] = dest

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
		imagePath = tempDir + '/' + appName + '.dmg'
		call(['hdiutil', 'create', '-srcfolder',  self.src, imagePath])

		DATA_FILES.append(imagePath)

		# py2app requires special arguments, the semi-standalone flag is being used
		# because it crashes without, however this makes the app rely on the python
		# that is installed on the system.
		oldArgs = sys.argv
		sys.argv = [oldArgs[0], 'py2app', '--semi-standalone']

		# create app
		#print 'Creating App'
		try:
			setup(
				app=APP,
				name=appName,
				data_files=DATA_FILES,
				options={'py2app': OPTIONS},
				setup_requires=['py2app']
			)
		except TypeError as e:
			shutil.rmtree(tempDir)
			return False
			#print 'App creation failed: ' + str(e)

		# Clean up temp directory
		# print 'Cleaning up'
		shutil.rmtree(tempDir)
		sys.argv = oldArgs # restore the old arguments
		return True

	def createWidgets(self):
		self.pack(padx=0, pady=0) # padding for the entire window
		self.configure(background=BG_COLOR)

		labelWidth = 18
		entryWidth = 45
		self.image = PhotoImage(file='logo.ppm', )
		Label(self, bg=BG_COLOR, foreground=FG_COLOR, image=self.image).pack(fill=BOTH, expand=True, padx=0, pady=0)

		# Source and Destination input
		pathFrame = Frame(self)
		pathFrame.configure(background=BG_COLOR)
		pathFrame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=10)

		Label(pathFrame, text='Path to Application:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(pathFrame, text='Path to Launcher:', bg=BG_COLOR, foreground=FG_COLOR, width=labelWidth, anchor=E).grid(row=1, column=0)

		self.srcEntry = Entry(pathFrame, highlightbackground=BG_COLOR, width=entryWidth-5, validate="focusout", validatecommand=self.getinfo)
		self.srcEntry.grid(row=0, column=1)
		self.destEntry = Entry(pathFrame, highlightbackground=BG_COLOR, width=entryWidth-5)
		self.destEntry.grid(row=1, column=1)

		Button(pathFrame, text='Browse', command=self.openFile, font="Arial 10", highlightbackground=BG_COLOR, pady=5, padx=2).grid(row=0, column=2)
		Button(pathFrame, text='Browse', command=self.openDir, font="Arial 10", highlightbackground=BG_COLOR, pady=5, padx=2).grid(row=1, column=2)

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

		self.shadowEntry = Entry(optionsFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.preflightEntry = Entry(optionsFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.postflightEntry = Entry(optionsFrame, highlightbackground=BG_COLOR, width=entryWidth)

		self.shadowEntry.grid(row=0, column=1)
		self.preflightEntry.grid(row=1, column=1)
		self.postflightEntry.grid(row=2, column=1)

		Button(self, text="Create", command=self.createApp, width=20, pady=5, highlightbackground=BG_COLOR).pack(pady=10)

	def __init__(self, master=None):
		Frame.__init__(self, master)

		# initialize variables
		self.src = ''
		self.file_opt = fileoptions = {}
		fileoptions['initialdir'] = '/Volumes/Data/Users/u0823377/'
		fileoptions['defaultextension'] = '.app'
		fileoptions['filetypes'] = [('apps', '.app'), ('All Files', '.*')]
		fileoptions['title'] = 'Open App'
		self.dir_opt = diroptions = {}
		diroptions['initialdir'] = '/Volumes/Data/Users/u/'
		diroptions['mustexist'] = True
		diroptions['title'] = 'Save Destination'

		self.createWidgets()

BG_COLOR="lightgrey"
FG_COLOR="black"
root = Tk()
root.configure(background=BG_COLOR)
app=Application(root)
app.mainloop()
