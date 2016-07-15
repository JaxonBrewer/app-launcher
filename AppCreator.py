import sys
import os
import plistlib
import shutil
import tempfile
from subprocess import call
from setuptools import setup

def buildApp(source):
	# Setup variables
	APP = ['appLauncher.py']
	DATA_FILES = []
	OPTIONS = {'argv_emulation': True}

	# Open App's info.plist so information can be extracted
	print 'Getting app info'
	appInfo = plistlib.readPlist(source + '/Contents/info.plist')

	appName = appInfo['CFBundleName']	
	appVersion = appInfo['CFBundleShortVersionString']
	appIconName = appInfo['CFBundleIconFile']

	# print information 
	'''	
	print appName
	print appVersion
	print appIconName
	'''


	# Custom information for info.plist
	print 'Creating info.plist'
	infoPlist = {'CFBundleShortVersionString': appVersion,
				 'CFBundleIdentifier': 'edu.utah.scl.' + appName.lower() + 'wrapper'}
	OPTIONS['plist'] = infoPlist

	# Append .icns to icon name from info.plist if not already there
	print 'Fetching app icon'
	if not appIconName.endswith('.icns'):
		appIconName += '.icns'
	iconPath = source + '/Contents/Resources/' + appIconName

	# Verify icon exists and add it to app setup
	if os.path.exists(iconPath):
		OPTIONS['iconfile'] = iconPath


	# Get destination to save app if not passed as arguement
	'''
	if not len(sys.argv) >= 4:
	
	else:
		destPath = sys.argv[3]
	'''
	destPath = raw_input('Destination folder: ') 
	# Check that destination is valid and add it to app setup
	if not os.path.exists(destPath):
		print 'Invalid Destination!'
		exit()	
	OPTIONS['dist_dir'] = destPath	

	# make tempory dir for image
	tempDir = tempfile.mkdtemp()

	# Create app image
	print 'Creating App image'
	imagePath = tempDir + '/' + appName + '.dmg'
	call(['hdiutil', 'create', '-srcfolder',  source, imagePath])
	
	DATA_FILES.append(imagePath)

	# create app
	print 'Creating App'
	try:
		setup(
			app=APP,
			name=appName,
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
# Get app directory if not passed in as argument
'''
if not len(sys.argv) >= 3:
	appPath = raw_input('Path to application: ')
else: 
	appPath = sys.argv[2]
'''
appPath = raw_input('Path to application: ')

# Check that the app is a valid directory
if os.path.exists(appPath):
	buildApp(appPath)
else:
	print 'Invalid source'


