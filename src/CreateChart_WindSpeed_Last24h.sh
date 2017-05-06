#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/WindSpeed_Last24h.png \
  -s 'now - 1 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v 'km/h' \
  -X 0 \
  --x-grid HOUR:1:HOUR:6:HOUR:1:0:%Hh \
  --color MGRID#FF0000 \
  --grid-dash 1:3 \
  DEF:winds9="$RRD_PATH":winds9:AVERAGE \
  LINE2:winds9#2A5931:'Windgeschwindigkeit'

sudo mv ../reports/WindSpeed_Last24h.png /var/www/html/reports/WindSpeed_Last24h.png
