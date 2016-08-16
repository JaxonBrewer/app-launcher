App Playpen
===========

A tool to quickly create a launcher for any Mac OS app that will launch the app in a sandboxed environment seperate from the host system.

## Download and Run

Simply pull the repo and run app\_creator\_ui.py with python. It has to be run from within the same directory as where AppLauncher.py resides or it is dependent on it and it  will not be able to locate it.

## System Requirements

App Playpen is intended to work on Mac OS. It should go back quite a few versions, but has not been tested beyond OS X 10.11 "El Capitan". 

The creator script requires python 2.7 and the py2app module to be installed. The launchers created by the script just require python 2.7
 
## Contact

If you have any comments, questions, or other input, either [file an issue](../../issues) or [send an email to us](mailto:mlib-its-mac-github@lists.utah.edu). Thanks!

## Purpose

App Playpen helps solve the problem of applications that do not play nicely in enterprise environment. A few examples would be applications that require updates everytime they start or require permissions that are unreasonable in a safely guarded enterprise environment. The App Playpen solves this problem by creating a wrapper for an application that launches the app in its own environment seperate from the host system. The launcher masquerades as the original application so there is no effect on the end user's experience with the application. 

## Usage

Start the script with python to open the UI
```
python app_creator_ui.py
```

This will give you a GUI where you can select the app you want to create a launcher for, and the destination folder where the launcher will be placed.
 
Below that section is a couple of fields that should be automatically populated when a valid app is selected. These are the info.plist values that will be used for the launcher. Should you want to change the name, version, or application icon, this section will allow you to do so with ease.

The last section has some additional options for more advanced use cases. The laucher works by mounting a image of the actual application and running it from there. Changes made to that image are stored in a shadow file with the same name as the launcher on the host system. The shadow path allows you to change the directory where the launcher's shadow file will be stored. The defualt location for the shadow file is in ```/tmp```.

The pre/postflight script fields allow you to run custom code before and after the application image has been mounted, but before the application is run. The pre/postflight scripts must be executables.
