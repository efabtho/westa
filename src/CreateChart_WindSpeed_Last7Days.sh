#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/WindSpeed_Last7Days.png \
  -s 'now - 7 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v 'km/h' \
  -X 0 \
  --x-grid HOUR:6:DAY:1:DAY:1:86400:%A \
  DEF:winds9="$RRD_PATH":winds9:AVERAGE \
  LINE2:winds9#2A5931:'Windgeschwindigkeit'

sudo mv ../reports/WindSpeed_Last7Days.png /var/www/html/reports/WindSpeed_Last7Days.png
