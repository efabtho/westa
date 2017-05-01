#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/AirPressure_Last7Days.png \
  -s 'now - 7 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v hPa \
  -X 0 \
  --y-grid 1:1 \
  --x-grid HOUR:6:DAY:1:DAY:1:86400:%A \
  DEF:psea="$RRD_PATH":psea:AVERAGE \
  LINE2:psea#8BBFFF:'Luftdruck'

sudo mv ../reports/AirPressure_Last7Days.png /var/www/html/reports/AirPressure_Last7Days.png

