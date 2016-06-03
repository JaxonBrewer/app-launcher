import sys
import os
import plistlib

#Get app Directory
appPath = raw_input("Path to application: ")

#Check that the app is a valid directory
if os.path.exists(appPath):
	appInfo = plistlib.readPlist(appPath + "/Contents/info.plist")

	appName = appInfo["CFBundleName"]	
	appVersion = appInfo["CFBundleShortVersionString"]
	appIconName = appInfo["CFBundleIconFile"]

	#append .icns if not already there
	if not appIconName.endswith(".icns"):
		appIconName += ".icns"
	iconPath = appPath + "/Contents/Resources/" + appIconName

	if not os.path.exists(iconPath):
		print "icon path invalid"
else:
	print "Invalid Directory"
