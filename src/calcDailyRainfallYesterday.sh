# set path variables
source /etc/environment

# Regenmenge des letzten Tages berechnen aus den abgespeicherten Wippenschlaegen des Regenmessers in der DB
rrdtool graph /dev/null \
  -s 'now'-24h -e 'now' \
  DEF:rains9="$RRD_PATH":rains9:AVERAGE \
  CDEF:rainpd=rains9,3600,*,24,*,0.295,* \
  VDEF:totalrain=rainpd,AVERAGE \
  PRINT:totalrain:"%6.1lf"|tail -1 > $1

sudo mv ./$1 /var/www/html/reports/$1
