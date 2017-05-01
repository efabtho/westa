#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/AirPressure_Last24h.png \
  -s 'now - 1 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v hPa \
  -X 0 \
  --x-grid HOUR:1:HOUR:6:HOUR:1:0:%Hh \
  --y-grid 1:1 \
  --color MGRID#FF0000 \
  --grid-dash 1:3 \
  DEF:psea="$RRD_PATH":psea:AVERAGE \
  LINE2:psea#8BBFFF:'Luftdruck'

sudo mv ../reports/AirPressure_Last24h.png /var/www/html/reports/AirPressure_Last24h.png
