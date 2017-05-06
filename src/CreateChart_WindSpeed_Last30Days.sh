#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/WindSpeed_Last30Days.png \
  -s 'now - 30 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v 'km/h' \
  -X 0 \
  DEF:winds9="$RRD_PATH":winds9:AVERAGE \
  LINE2:winds9#2A5931:'Windgeschwindigkeit'

sudo mv ../reports/WindSpeed_Last30Days.png /var/www/html/reports/WindSpeed_Last30Days.png
