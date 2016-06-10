import sys
import os
import plistlib
import shutil

# Get app directory
appPath = raw_input("Path to application: ")

# Check that the app is a valid directory
if os.path.exists(appPath):
	# Open App's info.plist so information can be extracted
	appInfo = plistlib.readPlist(appPath + "/Contents/info.plist")

	appName = appInfo["CFBundleName"]	
	appVersion = appInfo["CFBundleShortVersionString"]
	appIconName = appInfo["CFBundleIconFile"]

	# Append .icns to icon name from info.plist if not already there
	if not appIconName.endswith(".icns"):
		appIconName += ".icns"
	iconPath = appPath + "/Contents/Resources/" + appIconName

	# Get destination to save app
	destPath = raw_input("Destination folder: ") 

	# Create app directory
	newAppPath = destPath	
	if not newAppPath[-1] == '/':
		newAppPath += '/'
	newAppPath += appName + '.app'		
	os.makedirs(newAppPath)

	# Copy launcher template to the new directory
	shutil.copytree(os.path.realpath('ContentsTemplate'), newAppPath + '/Contents')

	# Edit new info.plist

	# Edit new applescript
	
	# Verify icon exists and trasfer it 
	if os.path.exists(iconPath):
		#TODO: Transfer icon	
		placeholder = 1
	else:
		print "Could not transfer app icon"

	# Create app image

else:
	print "Invalid Directory"
