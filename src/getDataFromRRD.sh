#!/bin/bash

# TFN 031216 v2 Anpassung an erweiterte rrd DB Struktur (Luftdruck) und DB Speicherort

RRD_PATH="/media/pi/HDD/data/weather2.rrd"

# uptime in Datei schreiben
uptime -p >> UserRQ_uptime.txt

# letzte abgespeicherte Daten aus der rrd DB in Datei schreiben
rrdtool lastupdate $RRD_PATH >> UserRQ_lastupdate.txt

# set WESTA_ACTIV_SRC variable (to get appropiate prod/dev sources)
source /etc/environment

# Datei UserRQ_lastupdate.txt auswerten und in einzelne txt-Datenschnipsel ausgeben
python $WESTA_ACTIV_SRC'makeDataFilesFromLastupdate.py'

# Datenschnipsel rüberschieben auf Web-Server
sudo mv ./UserRQ_*.txt /var/www/html/reports/

# Regenmenge der letzten 24h berechnen aus den abgespeicherten Wippenschlaegen des Regenmessers in der DB
rrdtool graph /dev/null \
  -s 'now'-24h -e 'now' \
  DEF:rains9="$RRD_PATH":rains9:AVERAGE \
  CDEF:rainpd=rains9,3600,*,24,*,0.295,* \
  VDEF:totalrain=rainpd,AVERAGE \
  PRINT:totalrain:"%6.0lf mm"|tail -1 > UserRQ_RainLast24h.txt

sudo mv ./UserRQ_RainLast24h.txt /var/www/html/reports/UserRQ_RainLast24h.txt
