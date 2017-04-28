#!/bin/bash

# get rid of resolution info text in log file
grep -v 1200x600 /media/pi/HDD/log/CronOutput/westa.log > /media/pi/HDD/log/CronOutput/westa2.log
mv /media/pi/HDD/log/CronOutput/westa2.log /media/pi/HDD/log/CronOutput/westa.log