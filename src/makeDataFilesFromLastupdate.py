#!/usr/bin/python -u
# -*- coding: utf-8 -*-

# TFN 291216 v4 Anpasssung an neue Sensorverteilung: Aussen->DG, RPi3 mit BMP180 ->Eltern-Sz
# TFN 011216 v3 Anpasssung an erweitertes Sensorfeld durch Aufnahme Luftdruck/Temp. vom BMP180

from __future__ import print_function

import datetime
import sys
from time import *


def main():
    # Datei mit letzten, gespeicherten Messwerten der rrd DB öffnen
    fh = open("UserRQ_lastupdate.txt","r")

    ZNr = 1

    for line in fh:
        # in dritter Zeile stehen der Messzeitpunkt und die Messwerte
        if ZNr == 3:
            line = line.strip()
            data = line.split(' ')
        ZNr += 1
    fh.close()

    # der Doppelpunkt stört hinter der Messzeit
    data[0] = data[0].rstrip(':')

    # Messwerte in Dateien schreiben für spaetere Anzeige

    # aktuelle Zeit festhalten
    fh = open("UserRQ_curTime.txt","w")
    print (strftime("%d-%m-%Y %H:%M:%S", localtime()), file=fh)
    fh.close()

    
    for i, val in enumerate(data):
        
        if i == 0: # Messzeitpunkt der Daten
            fh = open("UserRQ_timeStampOfValues.txt","w")
            print(datetime.datetime.fromtimestamp(int(val)).strftime('%d-%m-%Y %H:%M:%S'), file=fh)
            fh.close()

        if i == 1: # Temp. Dachgeschoss 
            fh = open("UserRQ_curTempTopFloor.txt","w")
            print(val,"°C", file=fh)
            fh.close()

        if i == 2: # Kellertemp.
            fh = open("UserRQ_curTempCellar.txt","w")
            print(val,"°C", file=fh)
            fh.close()

        if i == 9: # Luftfeuchtigkeit Dachgeschoss
            fh = open("UserRQ_curHumTopFloor.txt","w")
            print(val,"%", file=fh)
            fh.close()

        if i == 10: # Luftfeuchtigkeit Keller
            fh = open("UserRQ_curHumCellar.txt","w")
            print(val,"%", file=fh)
            fh.close()

        if i == 17: # Temp. Wettermast (Aussen)
            fh = open("UserRQ_curTempOutside.txt","w")
            print(val,"°C", file=fh)
            fh.close()

        if i == 18: # Luftfeuchtigkeit Wettermast (Aussen)
            fh = open("UserRQ_curHumOutside.txt","w")
            print(val,"%", file=fh)
            fh.close()

        if i == 19: # Windgeschw. Wettermast
            fh = open("UserRQ_curWindSpeedWM.txt","w")
            print(val,"km/h", file=fh)
            fh.close()

        if i == 21: # regnet es?
            fh = open("UserRQ_isRainingWM.txt","w")
            if val == "0":
                print("nein", file=fh)
            else:
                print("ja", file=fh)
            fh.close()

        if i == 22: # Temperatur vom BMP180 eingelesen (Luftdrucksensor), Standort = RPi3
            fh = open("UserRQ_curTempParBedroom.txt","w")
            print(val,"°C", file=fh)
            fh.close()

        if i == 23: # Luftdruck vom BMP180
            fh = open("UserRQ_curPressureSealevel.txt","w")
            print(val,"hPa", file=fh)
            fh.close()            
if __name__ == '__main__':
  main()
