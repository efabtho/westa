#!/bin/bash

RRD_PATH="/media/pi/HDD/data/weather2.rrd"
SENS_OUTS="temps9"

# set WESTA_ACTIV_SRC variable (to get appropiate prod/dev sources)
source /etc/environment

cd $WESTA_ACTIV_SRC

# Min. Temperatur der letzten 12h
rrdtool graph /dev/null -s 'now'-12h -e 'now' \
  DEF:"$SENS_OUTS"_act="$RRD_PATH":"$SENS_OUTS":AVERAGE \
  PRINT:"$SENS_OUTS"_act:MIN:"%4.1lf °C"|tail -1 > minTempNight.txt

sudo mv ./minTempNight.txt /var/www/html/reports/minTempNight.txt