#!/bin/bash

# TFN 240917 added generation of OWM based informations to txt files
# TFN 010517 environment settings and westa.log copied to web server to be shown in debug menu# TFN 031216 Anpassung an erweiterte rrd DB Struktur (Luftdruck) und DB Speicherort

# set path variables
source /etc/environment

# show source path to get it displayed under "debug info"
sudo cp /etc/environment /var/www/html/reports/environment.txt

# copy log file to web server to get it displayed under "debug info"
sudo cp /media/pi/HDD/log/CronOutput/westa.log /var/www/html/reports/westa.log

# uptime in Datei schreiben
uptime -p >> UserRQ_uptime.txt

# letzte abgespeicherte Daten aus der rrd DB in Datei schreiben
rrdtool lastupdate $RRD_PATH >> UserRQ_lastupdate.txt

# Datei UserRQ_lastupdate.txt auswerten und in einzelne txt-Datenschnipsel ausgeben
python $WESTA_ACTIV_SRC'makeDataFilesFromLastupdate.py'

# for debug...
pwd >> westa-server.log

# get OWM weather forecast data and write them to txt files (python3 only, see she-bang)
./getOWMWeatherForecast.py    >> westa-server.log 2>&1

# Regenmenge der letzten 24h berechnen aus den abgespeicherten Wippenschlaegen des Regenmessers in der DB
rrdtool graph /dev/null \
  -s 'now'-24h -e 'now' \
  DEF:rains9="$RRD_PATH":rains9:AVERAGE \
  CDEF:rainpd=rains9,3600,*,24,*,0.295,* \
  VDEF:totalrain=rainpd,AVERAGE \
  PRINT:totalrain:"%6.0lf mm"|tail -1 > UserRQ_RainLast24h.txt

# move all generated txt files to web server directory
sudo mv ./UserRQ_*.txt /var/www/html/reports/
