#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/TempMinMaxAvg_Last7Days.png \
  -s 'now - 7 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v '°C'\
  --x-grid HOUR:6:DAY:1:DAY:1:86400:%A \
  DEF:tempmins1="$RRD_PATH":temps9:MIN \
  DEF:tempmaxs1="$RRD_PATH":temps9:MAX \
  DEF:temps9="$RRD_PATH":temps9:AVERAGE \
  CDEF:tempranges1=tempmaxs1,tempmins1,- \
  LINE1:tempmins1#0000FF \
  AREA:tempranges1#8dadf588::STACK \
  LINE1:tempmaxs1#0000FF \
  LINE2:temps9#616066:'Außentemperatur (Min/Durchschnitt/Max)' \
  LINE1:30#C6913B \
  LINE1:20#C6913B \
  LINE1:10#C6913B \
  LINE2:0#C6913B

sudo mv ../reports/TempMinMaxAvg_Last7Days.png /var/www/html/reports/TempMinMaxAvg_Last7Days.png