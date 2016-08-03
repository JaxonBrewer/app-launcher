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
from subprocess import call

def launch():
	appInfo = plistlib.readPlist('../info.plist')
	appName = appInfo['CFBundleName']
	mountRoot = '/Volumes'
	diskName = appName
	appPath = mountRoot + '/' + diskName + '/' + appName + '.app'
	imagePath = os.path.realpath(appName + '.dmg')
	shadowPath = appInfo['ShadowPath']

	# Check that the app image is mounted, mount it if it is not
	if not os.path.ismount(mountRoot + '/' + diskName):
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


	# Launch application for user
	if os.path.exists(appPath):
		call(['/usr/bin/open', '-a', appPath])


launch()
