#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/AirPressure_Last90Days.png \
  -s 'now - 90 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v hPa \
  --x-grid WEEK:1:MONTH:1:MONTH:1:0:%B \
  -X 0 \
  --y-grid 1:1 \
  DEF:psea="$RRD_PATH":psea:AVERAGE \
  LINE2:psea#8BBFFF:'Luftdruck'

sudo mv ../reports/AirPressure_Last90Days.png /var/www/html/reports/AirPressure_Last90Days.png

