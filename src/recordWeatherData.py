#!/usr/bin/python -u
# -*- coding: utf-8 -*-

# TFN 120412 v15 using ConfigParser to get path to rrd database
# TFN 120317 v14 added counting for 'Regentage'
# TFN 260217 v13 extended module for some new statistic features ('Frosttage', 'Dauerfrosttage', 'Tropische Nächte', 'MaxDelta')
# TFN 220117 v12 substituted hard coded year, month info for db update
# TFN 190117 v10 added monthly min/max values
# TFN 190117 v9  using MySQLdb for storing min/max values
# TFN 031216 v8  Erweitert um Aufzeichnung von BMP180 Daten


# remarks:
# detection of day change is done only in seperate crontab task shortly after midnight to avoid unnecessary db handling
# detection is used for: adding new year record, init record for new month and calculating last days statistics
#
# ATTENTION: Before releasing this module, check table name in all relevant modules and turn off DEBUG mode!!!!!!!!!
#

import serial
import sys
import os
import rrdtool
import Adafruit_BMP.BMP085 as BMP085
import MySQLdb
import ConfigParser

from time import *
from decimal import *

DEBUG = False

# serial port of USB-WDE1
port = '/dev/ttyUSB0'

monthArray = ['Januar','Februar','März','April','Mai','Juni','Juli', 'August','September','Oktober','November','Dezember']


def checkMySQLdbUpdate(curTime, curTempOutside, curPsea, curWindSpeed, isRaining):
  if DEBUG:
    print "check for MySQLdb updates, current values...:"
    print "curTime:        ", curTime
    print "curTempOutside: ", curTempOutside
    print "curPsea:        ", curPsea
    print "curWindSpeed:   ", curWindSpeed
    print "isRaining:      ", isRaining

  # extract current month and year out of passed string 'curTime'
  curMonth = curTime.split('-')
  curYear = curMonth[2]
  curYear = curYear[0:4] # get rid of time info
  curMonth = int(curMonth[1]) # counts 1-12

  if DEBUG:
    print "curYear:        ", curYear
    print "curMonth:       ", curMonth

  try:
    db = MySQLdb.connect("localhost", "pi","","temps")
    curs = db.cursor()
    
    sql_update_query_MAX = \
      "UPDATE tbl_WeSta_values2 SET Wert = %s, Messzeitpunkt = %s WHERE Wert < %s \
        AND Sensor = %s AND Type = %s AND Periode = %s"

    sql_update_query_MIN = \
      "UPDATE tbl_WeSta_values2 SET Wert = %s, Messzeitpunkt = %s WHERE Wert > %s \
        AND Sensor = %s AND Type = %s AND Periode = %s"
  
    if curTempOutside != '': # valid value?
      curTempOutside = Decimal(curTempOutside.replace(',','.'))
      # check for MIN/MAX updates of records
      curs.execute(sql_update_query_MAX, \
        (curTempOutside, curTime, curTempOutside, 'Außentemperatur', 'max', 'all time'))
      curs.execute(sql_update_query_MIN, \
        (curTempOutside, curTime, curTempOutside, 'Außentemperatur', 'min', 'all time'))
      curs.execute(sql_update_query_MAX, \
        (curTempOutside, curTime, curTempOutside, 'Außentemperatur', 'max', curYear))
      curs.execute(sql_update_query_MIN, \
        (curTempOutside, curTime, curTempOutside, 'Außentemperatur', 'min', curYear))
      curs.execute(sql_update_query_MAX, \
        (curTempOutside, curTime, curTempOutside, 'Außentemperatur', 'max', monthArray[curMonth-1])) 
      curs.execute(sql_update_query_MIN, \
        (curTempOutside, curTime, curTempOutside, 'Außentemperatur', 'min', monthArray[curMonth-1]))
      curs.execute(sql_update_query_MAX, \
        (curTempOutside, curTime, curTempOutside, 'Außentemperatur', 'max', 'day')) # used to calc 'MaxDelta' after midnight
      curs.execute(sql_update_query_MIN, \
        (curTempOutside, curTime, curTempOutside, 'Außentemperatur', 'min', 'day')) # dito.

    if curWindSpeed != '':
      curWindSpeed = Decimal(curWindSpeed.replace(',','.'))
      # check for MIN/MAX updates of records
      curs.execute(sql_update_query_MAX, \
        (curWindSpeed, curTime, curWindSpeed, 'Windgeschwindigkeit', 'max', 'all time'))
      
    # check for MIN/MAX updates of records
    curs.execute(sql_update_query_MAX, \
      (curPsea, curTime, curPsea, 'Luftdruck', 'max', 'all time'))
    curs.execute(sql_update_query_MIN, \
      (curPsea, curTime, curPsea, 'Luftdruck', 'min', 'all time'))

    sql_update_query_SETFLAG = \
      "UPDATE tbl_WeSta_values2 SET Wert = %s, Messzeitpunkt = %s WHERE \
        Sensor = %s AND Type = %s AND Periode = %s"

    # check for "Frost_Erkannt" and "PlusGrade_Erkannt" to count for days with frost or perma frost conditions
    if curTempOutside <= 0:
      curs.execute(sql_update_query_SETFLAG, \
        (1, curTime, 'Frost_Erkannt', 'Flag', 'day'))
    else:
      curs.execute(sql_update_query_SETFLAG, \
        (1, curTime, 'PlusGrade_Erkannt', 'Flag', 'day'))
      
    # check for "Unter_20grd_Erkannt" to count for days with so-called "tropical nights"
    if curTempOutside < 20:
      curs.execute(sql_update_query_SETFLAG, \
        (1, curTime, 'Unter_20grd_Erkannt', 'Flag', 'day'))

    # check for "Regen_Erkannt" to count for days with rain fall
    if isRaining:
      curs.execute(sql_update_query_SETFLAG, \
        (1, curTime, 'Regen_Erkannt', 'Flag', 'day'))

    db.commit()

    if DEBUG:
      # print out db table content    
      print "\nDump table: tbl_WeSta_values2:"
      print "================================================================================"
      curs.execute("SELECT * FROM tbl_WeSta_values2 ORDER BY DisplayOrder ASC")
      for reading in curs.fetchall():
          print str(reading[0])+ " " + str(reading[1]) + " " + str(reading[2]) + " " + str(reading[3]) + " " \
                + str(reading[4]) + " " + str(reading[5]) + " " + str(reading[6]) + " " + str(reading[7]) + " " \
                + str(reading[8])
      print "db.close() and return to main()"

    db.close()
    
  except MySQLdb.Error, e:
    try:
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    except IndexError:
        print "MySQL Error: %s" % str(e)
           
    print "Error: will rollback database"
    db.rollback()
    db.close()

def main():
  if DEBUG:
    print "<<<<<<<<<start"

  # get rrd path
  config = ConfigParser.ConfigParser()
  config.read("/home/pi/westa-config.txt")
  rrdDatabase = config.get("path","RRD_Database")
    
  # Korrekturwerte zur Fehlerkompensation
  AirPressureCor = -1
  TempBMP180Cor  = -3

  # Luftdruck und Temp. Sensor BMP180 (085) am i2c bus
  sensor = BMP085.BMP085()

  # open serial line
  ser = serial.Serial(port, 9600)
  if not ser.isOpen():
    print "Error: Unable to open serial port %s" % port
    sys.exit(1)

  while(1==1):
    # Luftdruck einlesen und auf Meereshoehe korrigieren
    pressure = sensor.read_pressure()
  
    # Hoehe ueber Meeresspiegel fuer Sohldfeld
    altitude = 110
    # Korrigieren auf Meereshoehe und hPa
    psea = (pressure / pow(1.0 - altitude/44330.0, 5.255))/100
    psea = int(psea + 0.5)
    psea = psea + AirPressureCor

    # Temperaturwert einlesen
    temps10 = sensor.read_temperature()
    temps10 = round (temps10, 1)
    temps10 = temps10 + TempBMP180Cor

    if DEBUG:
      print "BMP180 values:"
      print "pressure      = ", pressure
      print "p at sealevel = ", psea
      print "temperature   = ", temps10

    # read line from WDE1
    if DEBUG:
      ##########################################vvv##############
      line = "$1;1;;18,2;16,0;;;;;;;63;64;;;;;;;0;85;0;351;0;0"
      ##########################################^^^##############
    else:
      line = ser.readline() # can take some time...
      
    line = line.strip()
    
    # save time stamp of new data set (do *not* change format - will be used in sub function!)
    curTime = strftime("%d-%m-%Y %H:%M:%S", localtime())
    
    if DEBUG:
      print "read from WDE1 =", line
      print "at: ", curTime

    data = line.split(';')

    if DEBUG:
      print "dump data array:"
      for i, val in enumerate(data):
        print("Index: %2d Wert: %s" % (i, val))

    if (len(data) == 25 and data[0] == '$1' and data[24] == '0'):
      # data is valid

      # check for min/max values and statistic data, persist them using MySBLdb
      curTempOutside = data[19]
      curWindSpeed = data[21]
      isRaining = False if data[23] == '0' else True
      checkMySQLdbUpdate(curTime, curTempOutside, psea, curWindSpeed, isRaining)
      
      # re-format data into an update string for rrdtool
      for i, val in enumerate(data):
        data[i] = ('U' if val == '' else val.replace(',', '.'))
      update = 'N:' + ':'.join(data[3:24])

      update = update + ':' + str(temps10) + ':' + str(psea)

      if DEBUG:
        print "insert 'Update' to rrd = ", update
        
      if not DEBUG: # while testing: no rrd manipulation
        # insert data into database
        rrdtool.update(rrdDatabase, update)
  
      # terminate the program - we get invoked regularly from cron
      if DEBUG:
        print "break"
        print "<<<<<<<<<end"
      break 

  ser.close()


if __name__ == '__main__':
  main()
