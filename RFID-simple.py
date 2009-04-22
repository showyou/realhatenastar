#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""Copyright 2008 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.5'
__date__ = 'October 23 2008'

"""
modified by showyou, April 22 2009
"""

# 星をつける対象のURLを指定してください
sUrl = "http://f.hatena.ne.jp/showyou/20090328044421"


#Basic imports
from ctypes import *
import sys
import addStar
#Phidget specific imports
from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.RFID import RFID

#Create an RFID object
rfid = RFID()

#Information Display Function
def displayDeviceInfo():
    print "|------------|----------------------------------|--------------|------------|"
    print "|- Attached -|-              Type              -|- Serial No. -|-  Version -|"
    print "|------------|----------------------------------|--------------|------------|"
    print "|- %8s -|- %30s -|- %10d -|- %8d -|" % (rfid.isAttached(), rfid.getDeviceType(), rfid.getSerialNum(), rfid.getDeviceVersion())
    print "|------------|----------------------------------|--------------|------------|"
    print "Number of outputs: %i -- Antenna Status: %s -- Onboard LED Status: %s" % (rfid.getOutputCount(), rfid.getAntennaOn(), rfid.getLEDOn())
    return 0

#Event Handler Callback Functions
def rfidAttached(e):
    attached = e.device
    print "RFID %i Attached!" % (attached.getSerialNum())
    return 0

def rfidDetached(e):
    detached = e.device
    print "RFID %i Detached!" % (detached.getSerialNum())
    return 0

def rfidError(e):
    print "Phidget Error %i: %s" % (e.eCode, e.description)
    return 0

def rfidOutputChanged(e):
    print "Output %i State: %s" % (e.index, e.state)
    return 0

def rfidTagGained(e):
    rfid.setLEDOn(1)
    print "Tag Read: %s" % (e.tag)
    addStar.SHatena(sUrl) 
    return 0

def rfidTagLost(e):
    rfid.setLEDOn(0)
    print "Tag Lost: %s" % (e.tag)
    return 0

#Main Program Code
try:
    rfid.setOnAttachHandler(rfidAttached)
    rfid.setOnDetachHandler(rfidDetached)
    rfid.setOnErrorhandler(rfidError)
    rfid.setOnOutputChangeHandler(rfidOutputChanged)
    rfid.setOnTagHandler(rfidTagGained)
    rfid.setOnTagLostHandler(rfidTagLost)
except PhidgetException, e:
    print "Phidget Exception %i: %s" % (e.code, e.message)
    print "Exiting...."
    exit(1)

print "Opening phidget object...."

try:
    rfid.openPhidget()
except PhidgetException, e:
    print "Phidget Exception %i: %s" % (e.code, e.message)
    print "Exiting...."
    exit(1)

print "Waiting for attach...."

try:
    rfid.waitForAttach(10000)
except PhidgetException, e:
    print "Phidget Exception %i: %s" % (e.code, e.message)
    try:
        rfid.closePhidget()
    except PhidgetException, e:
        print "Phidget Exception %i: %s" % (e.code, e.message)
        print "Exiting...."
        exit(1)
    print "Exiting...."
    exit(1)
else:
    displayDeviceInfo()

print "Turning on the RFID antenna...."
rfid.setAntennaOn(True)

print "Press Enter to quit...."

chr = sys.stdin.read(1)

try:
    lastTag = rfid.getLastTag()
    print "Last Tag: %s" % (lastTag)
except PhidgetException, e:
    print "Phidget Exception %i: %s" % (e.code, e.message)

print "Closing..."

try:
    rfid.closePhidget()
except PhidgetException, e:
    print "Phidget Exception %i: %s" % (e.code, e.message)
    print "Exiting...."
    exit(1)

print "Done."
exit(0)
