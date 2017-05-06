#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/Rain_Last24h.png \
  -s 'now - 24 h' -e 'now' \
  -v 'l/m2' \
  -w 1200 -h 600 -D \
  -X 0 \
  --x-grid HOUR:1:HOUR:6:HOUR:1:0:%Hh \
  --color MGRID#FF0000 \
  --grid-dash 1:3 \
  DEF:rains9="$RRD_PATH":rains9:AVERAGE \
  CDEF:rainph=rains9,3600,*,0.295,* \
  CDEF:rainpd=rainph,24,* \
  VDEF:totalrain=rainpd,AVERAGE \
  GPRINT:totalrain:"Total %6.0lf l/m2 in 24h" \
  LINE2:rainph#0000FF:'Regenmenge (1 l/m2 = 1 mm/m2)'

sudo mv ../reports/Rain_Last24h.png /var/www/html/reports/Rain_Last24h.png
