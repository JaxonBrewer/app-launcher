# Author: Jaxon Brewer
# Date: August 3, 2016
#
# Created for the Marriot Library at the University of Utah
#
# This script is used to wrap applications that behave poorly
# in a locked down evironment. It launches an application in a
# sandbox environment that has not effect on the host system
# of the application.

import os
import sys
import plistlib
import logging
from subprocess import call

#logging setup
LOG_FILE = os.path.expanduser('~/Library/Logs/app_playpen_launcher.log')
if not os.path.exists(os.path.dirname(LOG_FILE)):
	os.makedirs(os.path.dirname(LOG_FILE))
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

def launch():
	appInfo = plistlib.readPlist('../info.plist')
	appName = appInfo['CFBundleName']
	mountRoot = '/Volumes'
	diskName = appName
	appPath = mountRoot + '/' + diskName + '/' + appInfo['AppFileName']
	imagePath = os.path.realpath(appName + '.dmg')
	shadowPath = os.path.expanduser(appInfo['ShadowPath'])

	logging.info('preparing to launch ' + appName)

	#Create shadowpath directory if it does not already exist
	if not os.path.exists(os.path.dirname(shadowPath)):
		logging.info('Creating directories for shadow file at ' + os.path.dirname(shadowPath))
		os.makedirs(os.path.dirname(shadowPath))


	# execute the preflight script if it exists
	# NOTE there is a possible security risk here as this will execute anything,
	# it shouldn't be a problem if the app directory is write protected.
	if os.path.isfile("preflight"):
		try:
			logging.info('executing preflight script for ' + appName)
			execfile("preflight")
		except:
			logging.error('Preflight failed to execute properly')
	# Check that the app image is mounted, mount it if it is not
	if not os.path.ismount(mountRoot + '/' + diskName):
		logging.info('Mounting application image for ' + appName + ' at ' + mountRoot)
		''' Mount the image at imagePath with:
		 * -nobrowse		Prevents the volume from appearing in
		                   Finder or on the Desktop.
		 * -noautoopenro	Makes sure we won't accidentally pop
                           open a Finder window into the volume.
		 * -noverify		Ensures that hdiutil will not verify
                           the volume. Speeds up mount times.
		 * -mountroot		Changes where the volume is mounted to.
		 * -shadow			Allows read/write access by creating
                           a file the user can edit and shadowing
                           what would have been the edits there.'''
		call(['hdiutil', 'attach', '-nobrowse', '-owners', 'on', '-noautoopenro', '-noverify', '-mountroot',  mountRoot, '-shadow',  shadowPath, imagePath])

	# execute the postflight script if it exists
	if os.path.isfile("postflight"):
		try:
			logging.info('executing postflight script for ' + appName)
			execfile("postflight")
		except:
			logging.error('Postflight failed to execute properly')

	# Launch application for user
	if os.path.exists(appPath):
		logging.info('Launching real application at ' + appPath)
		call(['/usr/bin/open', '-a', appPath])
	else:
		logging.error('Could not launch real application. App not found at ' + appPath)

launch()
