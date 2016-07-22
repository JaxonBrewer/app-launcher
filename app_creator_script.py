import sys
import os
import shutil
import plistlib
from subprocess import call
from setuptools import setup


# Setup variables
APP = ['appLauncher.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True}

source = 
dest = self.src.get()

# Open App's info.plist so information can be extracted
print 'Getting app info'
appInfo = plistlib.readPlist(source + '/Contents/info.plist')

print self.appName

self.appName = appInfo['CFBundleName']	
self.appVersion = appInfo['CFBundleShortVersionString']
self.appIconName = appInfo['CFBundleIconFile']

print self.appName
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
if not os.path.exists(dest):
	print 'Invalid Destination!'
	exit()
OPTIONS['dist_dir'] = dest	

# make tempory dir for image
tempDir = tempfile.mkdtemp()

# Create app image
print 'Creating App image'
imagePath = tempDir + '/' + self.appName + '.dmg'
call(['hdiutil', 'create', '-srcfolder',  source, imagePath])

DATA_FILES.append(imagePath)
