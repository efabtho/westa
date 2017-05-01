#!/bin/bash

# outside temperature sensor
SENS_OUTS="temps9"

# set path variables
source /etc/environment

cd $WESTA_ACTIV_SRC

# Max. Temperatur der letzten 12h
rrdtool graph /dev/null -s 'now'-12h -e 'now' \
  DEF:"$SENS_OUTS"_act="$RRD_PATH":"$SENS_OUTS":AVERAGE \
  PRINT:"$SENS_OUTS"_act:MAX:"%4.1lf °C"|tail -1 > maxTempDay.txt

sudo mv ./maxTempDay.txt /var/www/html/reports/maxTempDay.txt