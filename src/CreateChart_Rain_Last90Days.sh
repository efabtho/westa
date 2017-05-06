#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/Rain_Last90Days.png \
  -s 'now - 90 days' -e 'now' \
  -v 'l/m2' \
  --x-grid WEEK:1:MONTH:1:MONTH:1:0:%B \
  -w 1200 -h 600 -D \
  -X 0 \
  DEF:rains9="$RRD_PATH":rains9:AVERAGE \
  CDEF:rainph=rains9,3600,*,0.295,* \
  CDEF:rainpd=rainph,24,* \
  CDEF:rainpm=rainpd,30,* \
  CDEF:rainpq=rainpm,3,* \
  VDEF:totalrain=rainpq,AVERAGE \
  GPRINT:totalrain:"Total %6.0lf l/m2 in 90 Tagen" \
  LINE2:rainpd#0000FF:'Regenmenge (1 l/m2 = 1 mm/m2)'

sudo mv ../reports/Rain_Last90Days.png /var/www/html/reports/Rain_Last90Days.png
