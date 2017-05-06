#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/WindSpeed_Last90Days.png \
  -s 'now - 90 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v 'km/h' \
  --x-grid WEEK:1:MONTH:1:MONTH:1:0:%B \
  -X 0 \
  DEF:winds9="$RRD_PATH":winds9:AVERAGE \
  LINE2:winds9#2A5931:'Windgeschwindigkeit'

sudo mv ../reports/WindSpeed_Last90Days.png /var/www/html/reports/WindSpeed_Last90Days.png
