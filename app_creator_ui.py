import os
import sys
import plistlib
import shutil
import tempfile
import ttk
import tkFileDialog
import PIL.Image
import PIL.ImageTk
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

		iconPath = self.src + '/Contents/Resources/' + appIconName
		if not iconPath.endswith('.icns'):
			iconPath += '.icns'
		im = PIL.Image.open(iconPath)
		newim = im.resize((32, 32))

		labelimage = PIL.ImageTk.PhotoImage(newim)
		self.iconPreview.configure(image=labelImage)
		self.iconPreview.image = labelImage

		return True

	def openFile(self):
		self.srcEntry.delete(0, END)
		self.srcEntry.insert(0, tkFileDialog.askopenfilename(**self.file_opt))
		self.getinfo()

	def openDir(self):
		self.destEntry.delete(0, END)
		self.destEntry.insert(0, tkFileDialog.askdirectory(**self.dir_opt))

	def createApp(self):
		# Setup variables
		APP = ['appLauncher.py']
		DATA_FILES = []
		OPTIONS = {'argv_emulation': True}

		# Custom information for info.plist
		infoPlist = {'CFBundleShortVersionString': self.longVersionEntry.get(),
					 'CFBundleIdentifier': 'edu.utah.scl.' + self.nameEntry.get().lower() + 'wrapper'}
		OPTIONS['plist'] = infoPlist

		dest = self.destEntry.get()
		if not os.path.exists(dest):
			# destination Invalid
			exit()
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
		imagePath = tempDir + '/' + self.nameEntry.get() + '.dmg'
		call(['hdiutil', 'create', '-srcfolder',  self.src, imagePath])

		DATA_FILES.append(imagePath)

		# py2app requires special arguments
		oldArgs = sys.argv
		sys.argv = [oldArgs[0], 'py2app', '--semi-standalone']

		# create app
		##print 'Creating App'
		try:
			setup(
				app=APP,
				name=self.nameEntry.get(),
				data_files=DATA_FILES,
				options={'py2app': OPTIONS},
				setup_requires=['py2app']
			)
		except TypeError as e:
			REMOVETHIS = "later"
			#print 'App creation failed: ' + str(e)

		# Clean up temp directory
		#print 'Cleaning up'
		shutil.rmtree(tempDir)
		sys.argv = oldArgs # restore the old arguments

	def createWidgets(self):
		self.pack(padx=10, pady=10) # padding for the entire window
		self.configure(background=BG_COLOR)

		labelWidth = 16
		entryWidth = 34
		# Source and Destination input
		pathFrame = Frame(self)
		pathFrame.configure(background=BG_COLOR)
		pathFrame.pack(side=TOP, fill=BOTH, expand=True)

		Label(pathFrame, text='Path to Application:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(pathFrame, text='Path to Launcher:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=1, column=0)

		self.srcEntry = Entry(pathFrame, highlightbackground=BG_COLOR, width=entryWidth, validate="focusout", validatecommand=self.getinfo)
		self.srcEntry.grid(row=0, column=1)
		self.destEntry = Entry(pathFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.destEntry.grid(row=1, column=1)

		Button(pathFrame, text='Browse', command=self.openFile, highlightbackground=BG_COLOR, pady=4).grid(row=0, column=2)
		Button(pathFrame, text='Browse', command=self.openDir, highlightbackground=BG_COLOR, pady=4).grid(row=1, column=2)

		self.s0 = ttk.Separator(self, orient=HORIZONTAL)
		self.s0.pack(side=TOP, fill=BOTH, pady=5)



		# App info preview and editor
		#self.image = PhotoImage(file='test.gif') #TODO: replace the preview image
		self.iconPreview = Label(self, bg=BG_COLOR).pack()

		# Default info plist attributes
		attributeFrame = Frame(self)
		attributeFrame.configure(background=BG_COLOR)
		attributeFrame.pack(side=TOP, fill=BOTH, expand=True)


		Label(attributeFrame, text='App Name:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(attributeFrame, text='Long Version Number:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=1, column=0)
		Label(attributeFrame, text='Short Version Number:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=2, column=0)
		Label(attributeFrame, text='Icon File:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=3, column=0)

		self.nameEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.longVersionEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.shortVersionEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)
		self.iconEntry = Entry(attributeFrame, highlightbackground=BG_COLOR, width=entryWidth)

		self.nameEntry.grid(row=0, column=1)
		self.longVersionEntry.grid(row=1, column=1)
		self.shortVersionEntry.grid(row=2, column=1)
		self.iconEntry.grid(row=3, column=1)


		self.s1 = ttk.Separator(self, orient=HORIZONTAL)
		self.s1.pack(side=TOP, fill=X, pady=5)


		# Options
		optionsFrame = Frame(self)
		optionsFrame.configure(background=BG_COLOR)
		optionsFrame.pack(side=TOP, fill=BOTH, expand=True)

		Label(optionsFrame, text='Shadow Path:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=0, column=0)
		Label(optionsFrame, text='Preflight:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=1, column=0)
		Label(optionsFrame, text='Postflight:', bg=BG_COLOR, width=labelWidth, anchor=E).grid(row=2, column=0)

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
		self.file_opt = fileoptions = {}
		fileoptions['initialdir'] = '/Volumes/Data/Users/u0823377/'
		fileoptions['defaultextension'] = '.app'
		fileoptions['filetypes'] = [('apps', '.app'), ('All Files', '.*')]
		fileoptions['title'] = 'Open App'
		self.dir_opt = diroptions = {}
		diroptions['initialdir'] = '/Volumes/Data/Users/u0823377/'
		diroptions['mustexist'] = True
		diroptions['title'] = 'Save Destination'

		self.createWidgets()

BG_COLOR="lightgrey"

root = Tk()
root.configure(background=BG_COLOR)
app=Application(root)
app.mainloop()
