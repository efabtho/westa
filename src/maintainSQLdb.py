#!/usr/bin/python -u
# -*- coding: utf-8 -*-

# TFN 180517 added debug info for logging 'wippensensor' counts (to verify rainfall calc)
# TFN 190317 v4 changes for counting days with rainfall
# TFN 190217 v3 this module will now to the folling things after being called after midnight
#               - setting counters coresponding to flags found in 'day' records
#               - analyzing yesterdays min/max temp. for calculating 'MaxDelta'
#               - doing inits for new day / new month / new year records
# TFN 190217 v2test preparing module for detecting further static data
#                   USE THIS VERSION FOR DATABASE INITS!!
#                   to do : - calling every midnight
# TFN 220117 v1 substituted hard coded year, month info for db update

# remarks:
# detection of day/month change is done only in this crontab controlled task (exec timing: 2 0 * * *)
# shortly after midnight
# detection is used for: adding new year records, init records for new month / new day
# This module also calculates the statistic data of last day
#
# DO *NOT* CALL THIS SCRIPT DIRECTLY WITHOUT THINKING ABOUT HOW TO AVOID OVERRIDING DATA!
# CHECK WHICH TABLE NAME IS USED!
#


import sys
import os
import MySQLdb

from datetime import date, timedelta
from time import *
from decimal import *

DEBUG_RAINFALL = True
DEBUG = False
TEST  = False

monthArray = ['Januar','Februar','März','April','Mai','Juni','Juli', 'August','September','Oktober','November','Dezember']


def main():

#  print "starting maintainSQLdb at: ", strftime("%d-%m-%Y %H:%M:%S", localtime())
     
  curYear  = strftime("%Y", localtime())
  curMonth = strftime("%m", localtime())
  curMonth = int(curMonth)
  curDay   = strftime("%d", localtime())
  curDay   = int(curDay)
  
  beforeCurMonth = curMonth - 1 # because we are called *after* midnight and data belongs to the day before...
  if beforeCurMonth == 0:
    beforeCurMonth = 12

  yesterday = (date.today() - timedelta(1)).strftime("%d-%m-%Y")
    
  if TEST:
    # only for module test:
    curDay = 1
    curMonth = 3
    beforeCurMonth = 2
    curYear = "2017"

  if DEBUG:
    print "curYear:        ", curYear
    print "curMonth:       ", monthArray[curMonth-1]
    print "beforeCurMonth: ", monthArray[beforeCurMonth-1]
    print "curDay:         ", curDay
    print "yesterday:      ", yesterday

  try:
    db = MySQLdb.connect("localhost", "pi","","temps")
    curs = db.cursor()

    # calc yesterdays rainfall using rrd data and write result to file
    subprocess.call(["/home/pi/westa/prod/src/calcDailyRainfallYesterday.sh", "DailyRainfallYesterday.txt"])
    
    # update monthly rainfall data with yesterdays rainfall
    # ...

    # counting days with rain fall
    curs.execute("SELECT * FROM tbl_WeSta_values2 WHERE Sensor = %s AND Wert = %s AND Periode = %s", \
      ('Regen_Erkannt','1.0','day',))
    results = curs.fetchall()
    # if last day was marked as 'Regen_Erkannt' then increment 'Regentage'
    if len(results) == 1:
      sql_update_query_INCR = \
          "UPDATE tbl_WeSta_values2 SET Wert = Wert + 1 WHERE \
           Sensor = %s AND Type = %s AND Periode = %s"
      curs.execute(sql_update_query_INCR, \
          ('Regenfall', 'Regentage', monthArray[curMonth-1] if curDay != 1 else monthArray[beforeCurMonth-1]))
      curs.execute(sql_update_query_INCR, \
          ('Regenfall', 'Regentage', (int(curYear)-1) if (curDay==1 and curMonth==1) else curYear ))
 
    # counting days with frost temperatures
    curs.execute("SELECT * FROM tbl_WeSta_values2 WHERE Sensor = %s AND Wert = %s AND Periode = %s", \
      ('Frost_Erkannt','1.0','day',))
    results = curs.fetchall()
    # if last day was marked as 'Frost_Erkannt' then increment 'Frosttage'
    if len(results) == 1:
      sql_update_query_INCR = \
          "UPDATE tbl_WeSta_values2 SET Wert = Wert + 1 WHERE \
           Sensor = %s AND Type = %s AND Periode = %s"
      curs.execute(sql_update_query_INCR, \
          ('Außentemperatur', 'Frosttage', monthArray[curMonth-1] if curDay != 1 else monthArray[beforeCurMonth-1]))
      curs.execute(sql_update_query_INCR, \
          ('Außentemperatur', 'Frosttage', (int(curYear)-1) if (curDay==1 and curMonth==1) else curYear ))
 
      # counting days with perma frost temperatures
      curs.execute("SELECT * FROM tbl_WeSta_values2 WHERE Sensor = %s AND Wert = %s AND Periode = %s", \
        ('PlusGrade_Erkannt','0.0','day',))
      results = curs.fetchall()
      # if last day was marked as 'Frost_Erkannt' and having no 'PlusGrade_Erkannt' then increment 'Dauerfrosttage'
      if len(results) == 1:
        sql_update_query_INCR = \
            "UPDATE tbl_WeSta_values2 SET Wert = Wert + 1 WHERE \
             Sensor = %s AND Type = %s AND Periode = %s"
        curs.execute(sql_update_query_INCR, \
            ('Außentemperatur', 'Dauerfrosttage', monthArray[curMonth-1] if curDay != 1 else monthArray[beforeCurMonth-1]))
        curs.execute(sql_update_query_INCR, \
            ('Außentemperatur', 'Dauerfrosttage', (int(curYear)-1) if (curDay==1 and curMonth==1) else curYear )) 

    # counting hot days with 'tropical night' conditions
    curs.execute("SELECT * FROM tbl_WeSta_values2 WHERE Sensor = %s AND Wert = %s AND Periode = %s", \
      ('Unter_20grd_Erkannt','0.0','day',))
    results = curs.fetchall()
    # if last day was not marked as 'Unter_20grd_Erkannt' then increment 'Tropische Nächte'
    if len(results) == 1:
      sql_update_query_INCR = \
          "UPDATE tbl_WeSta_values2 SET Wert = Wert + 1 WHERE \
           Sensor = %s AND Type = %s AND Periode = %s"
      curs.execute(sql_update_query_INCR, \
          ('Außentemperatur', 'Tropische Nächte', monthArray[curMonth-1] if curDay != 1 else monthArray[beforeCurMonth-1]))
      curs.execute(sql_update_query_INCR, \
          ('Außentemperatur', 'Tropische Nächte', (int(curYear)-1) if (curDay==1 and curMonth==1) else curYear ))

    # calculating maximum temperature diff of last day
    curs.execute("SELECT * FROM tbl_WeSta_values2 WHERE Sensor = %s AND Type = %s AND Periode = %s", \
      ('Außentemperatur', 'min', 'day',))
    for reading in curs.fetchall():
        dayMinTemp = reading[4]

    curs.execute("SELECT * FROM tbl_WeSta_values2 WHERE Sensor = %s AND Type = %s AND Periode = %s", \
      ('Außentemperatur', 'max', 'day',))
    for reading in curs.fetchall():
        dayMaxTemp = reading[4]

    deltaTemp = dayMaxTemp - dayMinTemp

    if DEBUG:
      print "dayMinTemp: ", dayMinTemp
      print "dayMaxTemp: ", dayMaxTemp
      print "deltaTemp:  ", deltaTemp

    # check for record updates if deltaTemp is greater than stored values in mysqldb 
    sql_update_query_MAX = \
      "UPDATE tbl_WeSta_values2 SET Wert = %s, Messzeitpunkt = %s WHERE Wert < %s \
      AND Sensor = %s AND Type = %s AND Periode = %s"

    curs.execute(sql_update_query_MAX, \
      (deltaTemp, yesterday, deltaTemp, 'Außentemperatur', 'MaxDelta', 'all time'))
    curs.execute(sql_update_query_MAX, \
      (deltaTemp, yesterday, deltaTemp, 'Außentemperatur', 'MaxDelta', monthArray[curMonth-1] if curDay != 1 else monthArray[beforeCurMonth-1]))
    curs.execute(sql_update_query_MAX, \
      (deltaTemp, yesterday, deltaTemp, 'Außentemperatur', 'MaxDelta', (int(curYear)-1) if (curDay==1 and curMonth==1) else curYear))
  
    db.commit()

    if curDay == 1:
      # we have a new month...
      if curMonth == 1:        
        # we have new year...
        curs.execute("SELECT * FROM tbl_WeSta_values2 WHERE Periode = %s",(curYear,))
        results = curs.fetchall()
        # if nothing found, add new records for the new year
        if len(results) == 0:
          sql_update_query_INIT_YEAR = \
              "INSERT INTO tbl_WeSta_values2(Visible, DisplayOrder, Sensor, Wert, Einheit, Type, Messzeitpunkt, Periode) \
              VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
          curs.execute(sql_update_query_INIT_YEAR, \
              ('J', 200, 'Außentemperatur', 100, '°C', 'min', 'none', curYear))
          curs.execute(sql_update_query_INIT_YEAR, \
              ('J', 200, 'Außentemperatur', -50, '°C', 'max', 'none', curYear))
          curs.execute(sql_update_query_INIT_YEAR, \
              ('J', 200, 'Außentemperatur', 0, '°C', 'MaxDelta', 'none', curYear))
          curs.execute(sql_update_query_INIT_YEAR, \
              ('J', 200, 'Außentemperatur', 0, 'Anzahl', 'Frosttage', 'n/a', curYear))
          curs.execute(sql_update_query_INIT_YEAR, \
              ('J', 200, 'Außentemperatur', 0, 'Anzahl', 'Dauerfrosttage', 'n/a', curYear))
          curs.execute(sql_update_query_INIT_YEAR, \
              ('J', 200, 'Außentemperatur', 0, 'Anzahl', 'Tropische Nächte', 'n/a', curYear))
          curs.execute(sql_update_query_INIT_YEAR, \
              ('J', 200, 'Regenfall', 0, 'Anzahl', 'Regentage', 'n/a', curYear))
          # set rainfall to zero for new year
          # ...
          print "***HAPPY NEW YEAR!*** added new year default records to db"
          
      # init month record with defaults to start the new min/max intervall of the new month
      sql_update_query_INIT_MONTH = \
          "UPDATE tbl_WeSta_values2 SET Wert = %s, Messzeitpunkt = %s WHERE \
           Sensor = %s AND Type = %s AND Periode = %s"
      curs.execute(sql_update_query_INIT_MONTH, \
          ("100.0", "none", 'Außentemperatur', 'min', monthArray[curMonth-1]))
      curs.execute(sql_update_query_INIT_MONTH, \
          ("-50.0", "none", 'Außentemperatur', 'max', monthArray[curMonth-1]))
      curs.execute(sql_update_query_INIT_MONTH, \
          ("0", "none", 'Außentemperatur', 'MaxDelta', monthArray[curMonth-1]))
      curs.execute(sql_update_query_INIT_MONTH, \
          ("0", "n/a", 'Außentemperatur', 'Frosttage', monthArray[curMonth-1]))
      curs.execute(sql_update_query_INIT_MONTH, \
          ("0", "n/a", 'Außentemperatur', 'Dauerfrosttage', monthArray[curMonth-1]))
      curs.execute(sql_update_query_INIT_MONTH, \
          ("0", "n/a", 'Außentemperatur', 'Tropische Nächte', monthArray[curMonth-1]))      
      curs.execute(sql_update_query_INIT_MONTH, \
          ("0", "n/a", 'Regenfall', 'Regentage', monthArray[curMonth-1]))
      # set rainfall to zero for new month
      # ...
      print "reinitialized records for new month: ", monthArray[curMonth-1]

    # init day records with defaults to start the new measurement intervall of the new day
    sql_update_query_INIT_DAY = \
        "UPDATE tbl_WeSta_values2 SET Wert = %s, Messzeitpunkt = %s WHERE \
         Sensor = %s AND Type = %s AND Periode = %s"
    curs.execute(sql_update_query_INIT_DAY, \
        ("100", "none", 'Außentemperatur', 'min', 'day'))
    curs.execute(sql_update_query_INIT_DAY, \
        ("-50", "none", 'Außentemperatur', 'max', 'day'))
    curs.execute(sql_update_query_INIT_DAY, \
        ("0", "none", 'Frost_Erkannt', 'Flag', 'day'))
    curs.execute(sql_update_query_INIT_DAY, \
        ("0", "none", 'PlusGrade_Erkannt', 'Flag', 'day'))
    curs.execute(sql_update_query_INIT_DAY, \
        ("0", "none", 'Unter_20grd_Erkannt', 'Flag', 'day'))
    curs.execute(sql_update_query_INIT_DAY, \
        ("0", "none", 'Regen_Erkannt', 'Flag', 'day'))
    if DEBUG:
      print "reinitialized record values for new day: ", curDay

    db.commit()

    
    if DEBUG:
      # print out db table content    
      print "\nDump table: tbl_WeSta_values2:"
      print "================================================================================"
      curs.execute("SELECT * FROM tbl_WeSta_values2 ORDER BY DisplayOrder ASC")
      for reading in curs.fetchall():
          print str(reading[0])+ "\t" + str(reading[1]) + "\t" + str(reading[2]) + "\t" + str(reading[3]) + "\t" \
                + str(reading[4]) + " " + str(reading[5]) + " " + str(reading[6]) + " " + str(reading[7]) + " " \
                + str(reading[8])
      print "db.close() and return to main()"

    db.close()
    
#    print "ending maintainSQLdb at: ", strftime("%d-%m-%Y %H:%M:%S", localtime())
  
    if DEBUG_RAINFALL:  
      os.system('rrdtool lastupdate /media/pi/HDD/data/weather2.rrd > /home/pi/westa/dev/reports/UserRQ_lastupdate.txt')
      i = 1
      fileRd = open("/home/pi/westa/dev/reports/UserRQ_lastupdate.txt","r")
      for line in fileRd:
        output = line.rstrip()
        if i == 3:
          lastupdate = output
        i = i+1
      print "rrd lastupdate @", strftime("%d-%m-%Y %H:%M:%S", localtime()), "is >>", lastupdate
    
  except MySQLdb.Error, e:
    try:
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    except IndexError:
        print "MySQL Error: %s" % str(e)
           
    print "Error: will rollback database"
    db.rollback()
    db.close()

if __name__ == '__main__':
  main()
