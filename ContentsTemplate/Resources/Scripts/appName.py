import os
import sys
import plistlib

appInfo = plistlib.readPlist(sys.argv[1] + 'Contents/info.plist')
print appInfo['CFBundleName']
