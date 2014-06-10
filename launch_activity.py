#!/usr/bin/python
__author__ = 'bincker'
#-*- coding: gbk -*-

import os
import argparse
import sys
import time
import subprocess


apkurl = sys.argv[1]

device = " emulator-5554"

#set tools dir
adb = "/Users/bincker/Desktop/android-sdk/sdk/platform-tools/adb"
aapt = "/Users/bincker/Desktop/android-sdk/sdk/build-tools/android-4.4/aapt"

#start adb
os.system(adb+" start-server")
if len(sys.argv) == 3 :
	device = " -s "+sys.argv[2]+":5555"
	os.system(adb+" connect "+sys.argv[2])

#read apkinfo
apkinfo = os.popen(aapt+" d badging "+ apkurl)
apkinfo = apkinfo.read()

print "read apkinfo"
#get apkname
start = apkinfo.find("package")
end = apkinfo.find("versionCode",start)
apkpackage = apkinfo[start:end-1]
apkname = apkpackage[apkpackage.find("'")+1:apkpackage.rfind("'")]


#get launch activity
start = apkinfo.find("launchable-activity")
end = apkinfo.find("label",start)
apkactivity = apkinfo[start:end-1]
apkactivity = apkactivity[apkactivity.find("'")+1:apkactivity.rfind("'")]


'''
if os.path.exists("results") == False:
	os.mkdir("results")

timeformat = "%y_%m_%d-%X"
testdir = "/TEST_"+time.strftime(timeformat)
if os.path.exists("results/"+apkname) == False:
	os.mkdir("results/"+apkname)
os.mkdir("results/"+apkname+testdir)

netdir = "results/"+apkname+testdir+"/network_traffic.pcap"
'''

os.system(adb+" -s "+device+" shell input keyevent 82")

print "install apk"

#install apk
os.system(adb+" -s "+device+" install "+apkurl)

print "launch apk"
#launch apk
os.system(adb+" -s "+device+" shell am start -W "+apkname+"/"+apkactivity)

time.sleep(60)

print "begin sending gestures"
#send gestures
print time.ctime()
os.system(adb+" -s "+device+" shell monkey -p "+apkname+" 1000")
print time.ctime()

print "unistall apk"
#unistall apk
os.system(adb+" -s "+device+" uninstall "+apkname)
