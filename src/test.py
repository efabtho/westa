#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys, os
from time import *

os.system('rrdtool lastupdate /media/pi/HDD/data/weather2.rrd > /home/pi/westa/dev/reports/UserRQ_lastupdate.txt')
i = 1
fileRd = open("/home/pi/westa/dev/reports/UserRQ_lastupdate.txt","r")
for line in fileRd:
  output = line.rstrip()
  if i == 3:
    lastupdate = output
  i = i+1
print "rrd lastupdate @", strftime("%d-%m-%Y %H:%M:%S", localtime()), "is >>", lastupdate

