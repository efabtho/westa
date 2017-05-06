#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/Humidity_Last90Days.png \
  -s 'now - 90 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v '%' \
  --x-grid WEEK:1:MONTH:1:MONTH:1:0:%B \
  DEF:hums1="$RRD_PATH":hums1:AVERAGE \
  LINE2:hums1#E04000:'Dachgeschoss' \
  DEF:hums2="$RRD_PATH":hums2:AVERAGE \
  LINE2:hums2#0000FF:'Keller' \
  DEF:hums9="$RRD_PATH":hums9:AVERAGE \
  LINE2:hums9#616066:'Aussen (Wettermast)' \

sudo mv ../reports/Humidity_Last90Days.png /var/www/html/reports/Humidity_Last90Days.png