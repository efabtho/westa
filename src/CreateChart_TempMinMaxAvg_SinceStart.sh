#!/bin/bash

RRD_PATH="/media/pi/HDD/data/weather2.rrd"

rrdtool graph ../reports/TempMinMaxAvg_SinceStart.png \
  -s '20170101' -e 'now' \
  -w 1200 -h 600 -D \
  -v '°C'\
  --x-grid WEEK:1:MONTH:1:MONTH:1:0:%B \
  DEF:tempmins1="$RRD_PATH":temps9:MIN \
  DEF:tempmaxs1="$RRD_PATH":temps9:MAX \
  DEF:temps9="$RRD_PATH":temps9:AVERAGE \
  CDEF:tempranges1=tempmaxs1,tempmins1,- \
  LINE1:tempmins1#0000FF \
  AREA:tempranges1#8dadf588::STACK \
  LINE1:tempmaxs1#0000FF \
  LINE2:temps9#0000FF:'Aussentemperatur (Min/Durchschnitt/Max)' \
  LINE1:0#C6913B

sudo mv ../reports/TempMinMaxAvg_SinceStart.png /var/www/html/reports/TempMinMaxAvg_SinceStart.png