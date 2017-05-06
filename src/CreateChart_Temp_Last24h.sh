#!/bin/bash

# set path variables 
source /etc/environment

cd $WESTA_ACTIV_SRC

rrdtool graph ../reports/Temp_Last24h.png \
  -s 'now - 1 day' -e 'now' \
  -w 1200 -h 600 -D \
  -v °C \
  --x-grid HOUR:1:HOUR:6:HOUR:1:0:%Hh \
  --color MGRID#FF0000 \
  --grid-dash 1:3 \
  DEF:temps1="$RRD_PATH":temps1:AVERAGE \
  LINE2:temps1#E04000:'Dachgeschoss' \
  DEF:temps2="$RRD_PATH":temps2:AVERAGE \
  LINE2:temps2#0000FF:'Keller' \
  DEF:temps10="$RRD_PATH":temps10:AVERAGE \
  LINE2:temps10#7FB37C:'Eltern-Sz' \
  DEF:temps9="$RRD_PATH":temps9:AVERAGE \
  LINE2:temps9#616066:'Aussen (Wettermast)' \
  LINE1:0#C6913B

sudo mv ../reports/Temp_Last24h.png /var/www/html/reports/Temp_Last24h.png