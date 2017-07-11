# set path variables
source /etc/environment

# Regenmenge eines Monats berechnen aus den abgespeicherten Wippenschlaegen des Regenmessers in der DB
rrdtool graph /dev/null \
  -s '00:00 01.01.2017' -e '00:00 01.02.2017' \
  DEF:rains9="$RRD_PATH":rains9:AVERAGE \
  CDEF:rainph=rains9,3600,*,0.295,* \
  CDEF:rainpd=rainph,24,* \
  CDEF:rainpm=rainpd,31,* \
  VDEF:totalrain=rainpm,AVERAGE \
  PRINT:totalrain:"%6.1lf mm"|tail -1 > MonthlyRainfall.txt

cat MonthlyRainfall.txt
