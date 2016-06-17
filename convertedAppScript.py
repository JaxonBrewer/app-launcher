# Author: Jaxon Brewer
# 
# Created for the Marriot Library at the University of Utah
#
# This script is used to wrap applications that behave poorly
# in a locked down evironment.It launches an application in a
# sandbox environment that has not effect on the host system
# of the application.

import os
import sys
import getpass
from subprocess import call

def isRunning():
	# placeholder for now
	return False

def launch():
	myPath = os.path.realpath(__file__)
	appName = 'APP_NAME'
	diskName = appName
	appPath = diskName + '/' + appName + '.app'
	imagePath = myPath + '/Contents/Resources/' + appName + '.dmg'
	shadowPath = '/tmp/' + appName + '.shadow'
	binName = appPath + '/Contents/MacOS/nwjs'
	mountRoot = '/Volumes'
	currentUser = getpass.getuser()
	reownScript = '/usr/local/bin/' + appName.lower() + '_change_owner.sh'

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
		call(['hdiutil', 'attach', '-nobrowse', '-owners on', '-noautoopenro', 'noverify', '-mountroot ' + mountRoot, '-shadow ' + shadowPath, imagePath])

		call(['sudo', reownScript, currentUser])
	
	# Launch application for user
	if os.path.exists(appPath):
		# * -W	Causes open to block until app exits
		# * -n	opens a new instance of the app
		call(['/usr/bin/open', '-W', '-n', '-a ' + appPath])



if isRunning():
	print "app is already running"
	#TODO: Make this better
else:
	launch()



