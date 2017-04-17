# -*- coding: utf-8 -*-
# TFN 170417 adding html file with long term statistics
# TFN 170413 using ConfigParser for email account data access
# TFN 170408 continuing work on this
# TFN 170402 send html based weather report email to get rid of umlaut problems...
# TFN 170120 added txt file with long term statistic data
# TFN xxxxxx append png file to email

from __future__ import print_function

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.header import Header
import smtplib
import subprocess
import ConfigParser

DEBUG = False

def mailWeatherReport():
    # RPi3 weather station dedicated email account
    config = ConfigParser.ConfigParser()
    config.read("/home/pi/westa-config.txt")
    strPassword   = config.get("mailConfig","Password")
    strFrom       = config.get("mailConfig","Username")
    strTo         = config.get("mailConfig","Sender")
    SMTPHostName  = config.get("mailConfig","SMTPHostName")
    Port          = config.get("mailConfig","Port")

    # export most recent rrd data set to txt files
    subprocess.call("/var/www/html/CallGetDataFromRRD.sh")

    # generate html file with long term statistics (used as attachment to weather report email)
    subprocess.call("/var/www/html/CallGenerateStatisticTable.sh")

    # import data sets into varables 
    fobj = open("/var/www/html/reports/UserRQ_timeStampOfValues.txt")
    for line in fobj:
        TimeStampOfValues =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_curTempOutside.txt")
    for line in fobj:
        curTempOutside =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_curHumOutside.txt")
    for line in fobj:
        curHumOutside =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_curPressureSealevel.txt")
    for line in fobj:
        curPressureSealevel =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_curWindSpeedWM.txt")
    for line in fobj:
        curWindSpeedWM =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_RainLast24h.txt")
    for line in fobj:
        RainLast24h =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_isRainingWM.txt")
    for line in fobj:
        isRainingWM =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/maxTempDay.txt")
    for line in fobj:
        maxTempDay =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/minTempNight.txt")
    for line in fobj:
        minTempNight =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_curTempParBedroom.txt")
    for line in fobj:
        curTempParBedroom =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_curTempTopFloor.txt")
    for line in fobj:
        curTempTopFloor =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_curHumTopFloor.txt")
    for line in fobj:
        curHumTopFloor =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_curTempCellar.txt")
    for line in fobj:
        curTempCellar =line.rstrip()
    fobj.close()

    fobj = open("/var/www/html/reports/UserRQ_curHumCellar.txt")
    for line in fobj:
        curHumCellar =line.rstrip()
    fobj.close()


    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = Header('Wetterbericht Sohldfeld: T_act= %s, T_NightMin= %s' % (curTempOutside, minTempNight),'utf-8')
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('Die aktuelle Wetterlage zu Hause...', _charset='utf-8')
    msgAlternative.attach(msgText)

    htmlTextBody = '\
        <!doctype html>\
        <html>\
            <head>\
                <style>\
                    body {\
                        background-color: #e0e0e0;\
                        font-family: Arial;\
                    }\
                    table, th, td {\
                        border: 1px solid black;\
                        border-collapse: collapse;\
                        height: 30px;\
                    }\
                    #tabelle        {background-color: antiquewhite}\
                    #ueberschrift   {background-color: #d0d0d2; color: black}\
                    #zeilengruppe   {background-color: navajowhite; color: black}\
                    .kursiv         {font-style: italic;}\
                    th, td          {padding: 2px;}\
                    th              {text-align: left;}\
                    td              {text-align: left;}\
                </style>\
                <meta charset="utf-8">\
            </head>\
            <table id="tabelle">\
                <caption>Alle Messdaten vom ' + TimeStampOfValues + '</caption>\
                <tbody id="zeilengruppe">\
                    <tr>\
                        <td>Außentemperatur:</td>\
                        <td>' + curTempOutside + '</td>\
                    </tr>\
                    <tr>\
                        <td>Luftfeuchtigkeit (Aussen):</td>\
                        <td>' + curHumOutside + '</td>\
                    </tr>\
                </tbody>\
                <tr>\
                    <td>Luftdruck:</td>\
                    <td>' + curPressureSealevel + '</td>\
                </tr>\
                <tr>\
                    <td>Windgeschwindigkeit:</td>\
                    <td>' + curWindSpeedWM + '</td>\
                </tr>\
                <tbody id="zeilengruppe">\
                    <tr>\
                        <td>Niederschlagsmenge der letzten 24h:</td>\
                        <td>' + RainLast24h + '</td>\
                    </tr>\
                    <tr>\
                        <td>Regnet es aktuell?</td>\
                        <td>' + isRainingWM + '</td>\
                    </tr>\
                </tbody>\
                <tr>\
                    <td>Tageshöchsttemperatur (6h-18h):</td>\
                    <td>' + maxTempDay + '</td>\
                </tr>\
                <tr>\
                    <td>Nächtliche Tiefsttemperatur (18h-6h):</td>\
                    <td>' + minTempNight + '</td>\
                </tr>\
                <tbody id="zeilengruppe">\
                    <tr>\
                        <td>Temperatur Eltern-Schlafzimmer:</td>\
                        <td>' + curTempParBedroom + '</td>\
                    </tr>\
                </tbody>\
                <tr>\
                    <td>Temperatur Dachgeschoss:</td>\
                    <td>' + curTempTopFloor + '</td>\
                </tr>\
                <tr>\
                    <td>Luftfeuchtigkeit Dachgeschoss:</td>\
                    <td>' + curHumTopFloor + '</td>\
                </tr>\
                <tbody id="zeilengruppe">\
                    <tr>\
                        <td>Temperatur Keller:</td>\
                        <td>' + curTempCellar + '</td>\
                    </tr>\
                    <tr>\
                        <td>Luftfeuchtigkeit Keller:</td>\
                        <td>' + curHumCellar + '</td>\
                    </tr>\
                </tbody>\
            </table>\
            <br><caption>Außentemperaturverlauf der letzten 24h</caption>\
            <br><img src="cid:image1">\
            <br><br><caption>Luftdruckverlauf der letzten 24h</caption>\
            <br><img src="cid:image2">\
            <br><br><caption>Außentemperaturverlauf der letzten 7 Tage</caption>\
            <br><img src="cid:image3">\
            </html>'
    
    if DEBUG:
        fh = open("DEBUG_htmlTextBody_for_WeatherReport.html","w")
        print (htmlTextBody, file=fh)
        fh.close()
        
    msgText = MIMEText(htmlTextBody, 'html','utf-8')
    msgAlternative.attach(msgText)
                       
    # attach image and use reference from above
    fp = open('/var/www/html/reports/Temp_Last24h.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # attach image and use reference from above
    fp = open('/var/www/html/reports/AirPressure_Last24h.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image2>')
    msgRoot.attach(msgImage)

    # attach image and use reference from above
    fp = open('/var/www/html/reports/Temp_Last7Days.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image3>')
    msgRoot.attach(msgImage)

    # attach html file with long term statistics
    msgHTMLAttachment = MIMEText(file("/var/www/html/html/min-max-values_generated.html").read(),'html', 'utf-8')
    msgHTMLAttachment.add_header('Content-Disposition','attachment', filename='min-max-values_generated.html')
    msgRoot.attach(msgHTMLAttachment)
    
    # Send the email (this example assumes SMTP authentication is required)
    smtp = smtplib.SMTP(SMTPHostName, Port)

    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo

    smtp.login(strFrom, strPassword)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()

if __name__ == '__main__':
    mailWeatherReport()
