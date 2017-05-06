#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/Rain_Last7Days.png \
  -s 'now - 7 days' -e 'now' \
  -v 'l/m2' \
  -w 1200 -h 600 -D \
  -X 0 \
  --x-grid HOUR:6:DAY:1:DAY:1:86400:%A \
  DEF:rains9="$RRD_PATH":rains9:AVERAGE \
  CDEF:rainph=rains9,3600,*,0.295,* \
  CDEF:rainpd=rainph,24,* \
  CDEF:rainpw=rainpd,7,* \
  VDEF:totalrain=rainpw,AVERAGE \
  GPRINT:totalrain:"Total %6.0lf l/m2 in 7 Tagen" \
  LINE2:rainpd#0000FF:'Regenmenge (1 l/m2 = 1 mm/m2)'

sudo mv ../reports/Rain_Last7Days.png /var/www/html/reports/Rain_Last7Days.png
