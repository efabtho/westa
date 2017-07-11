# set path variables
source /etc/environment

# Regenmenge des letzten Tages berechnen aus den abgespeicherten Wippenschlaegen des Regenmessers in der DB
rrdtool graph /dev/null \
  -s '00:00 10.07.2017' -e '00:00 11.07.2017' \
  DEF:rains9="$RRD_PATH":rains9:AVERAGE \
  CDEF:rainpd=rains9,3600,*,24,*,0.295,* \
  VDEF:totalrain=rainpd,AVERAGE \
  PRINT:totalrain:"%6.1lf mm"|tail -1 > DailyRainfall.txt

cat DailyRainfall.txt

