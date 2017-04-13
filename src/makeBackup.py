# -*- coding: utf-8 -*-
from datetime import date
import sys
import shutil


DEBUG = False


# Aktuelles Datum holen
Heute = date.today()

rrdPath       = "/media/pi/HDD/data/weather2.rrd"
rrdBackupPath = "/home/pi/westa/prod/backup"
statiticFile  = "/var/www/html/html/min-max-values_generated.html"

# weekday: 0 = Montag, ..., 6 = Sonntag
if DEBUG:
    print Heute.weekday()

# taegliches Backup der rrd DB machen auf die externe HDD
# ebenso für mySQLDB Historiendaten
# Zielsetzung: alle wesentlichen Daten auf zwei SDCards haben
if Heute.weekday()   == 0:
    shutil.copy2(rrdPath, rrdBackupPath+"/mo")
    shutil.copy2(statiticFile, rrdBackupPath+"/mo")
elif Heute.weekday() == 1:
    shutil.copy2(rrdPath, rrdBackupPath+"/di")
    shutil.copy2(statiticFile, rrdBackupPath+"/di")
elif Heute.weekday() == 2:
    shutil.copy2(rrdPath, rrdBackupPath+"/mi")
    shutil.copy2(statiticFile, rrdBackupPath+"/mi")
elif Heute.weekday() == 3:
    shutil.copy2(rrdPath, rrdBackupPath+'/do')
    shutil.copy2(statiticFile, rrdBackupPath+'/do')
elif Heute.weekday() == 4:
    shutil.copy2(rrdPath, rrdBackupPath+"/fr")
    shutil.copy2(statiticFile, rrdBackupPath+"/fr")
elif Heute.weekday() == 5:
    shutil.copy2(rrdPath, rrdBackupPath+"/sa")
    shutil.copy2(statiticFile, rrdBackupPath+"/sa")
elif Heute.weekday() == 6:
    shutil.copy2(rrdPath, rrdBackupPath+"/so")
    shutil.copy2(statiticFile, rrdBackupPath+"/so")
    
