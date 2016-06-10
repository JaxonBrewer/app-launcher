import sys
import os
import plistlib
import shutil

# Get app directory
if not len(sys.argv) >= 2:
	appPath = raw_input("Path to application: ")
else: 
	appPath = sys.argv[1]

# Check that the app is a valid directory
if os.path.exists(appPath):
	# Open App's info.plist so information can be extracted
	appInfo = plistlib.readPlist(appPath + "/Contents/info.plist")

	appName = appInfo["CFBundleName"]	
	appVersion = appInfo["CFBundleShortVersionString"]
	appIconName = appInfo["CFBundleIconFile"]

	# print information 
	print appName
	print appVersion
	print appIconName

	# Append .icns to icon name from info.plist if not already there
	if not appIconName.endswith(".icns"):
		appIconName += ".icns"
	iconPath = appPath + "/Contents/Resources/" + appIconName

	# Get destination to save app
	if not len(sys.argv) >= 3:
		destPath = raw_input("Destination folder: ") 
	else:
		destPath = sys.argv[2]


	# Create app directory
	newAppPath = destPath	
	if not newAppPath[-1] == '/':
		newAppPath += '/'
	newAppPath += appName + '.app'		
	os.makedirs(newAppPath)

	# Copy launcher template to the new directory
	shutil.copytree(os.path.realpath('ContentsTemplate'), newAppPath + '/Contents')

	# Edit new info.plist
	plistPath = newAppPath + '/Contents/info.plist'
	newPlist = plistlib.readPlist(plistPath)
	newPlist['CFBundleName'] = appName
	newPlist['CFBundleShortVersionString'] = appVersion
	newPlist['CFBundleIconFile'] = appIconName
	newPlist['CFBundleIdentifier'] = 'edu.utah.scl.' + appName + 'wrapper'
	plistlib.writePlist(newPlist, plistPath)

	# Verify icon exists and trasfer it 
	if os.path.exists(iconPath):
		#TODO: Transfer icon	
		placeholder = 1
	else:
		print "Could not transfer app icon"

	# Create app image
	os.system('hdiutil create -srcfolder ' + appPath + ' ' + newAppPath + '/Contents/Resources/' + appName + '.dmg')
else:
	print "Invalid Directory"

