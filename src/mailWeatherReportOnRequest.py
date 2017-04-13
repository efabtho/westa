# -*- coding: utf-8 -*-
# v6 TFN 170412 using ConfigParser for login data hiding from source code
# v5 TFN 170408 now using html based mailWeatherReport() function version (v9)

import imaplib, os
import re
import sys
from time import *
import datetime
import ConfigParser


# path to mailWeatherReport() - only if not in same source dir
# sys.path.append('/home/pi/Desktop/Projekt-WeSta/src/mail')

from mailWeatherReport import mailWeatherReport

DEBUG = False

# RPi3 weather station dedicated email account
config = ConfigParser.ConfigParser()
config.read("/home/pi/westa-config.txt")
Password   = config.get("mailConfig","Password")
Username   = config.get("mailConfig","Username")
Sender     = config.get("mailConfig","Sender")
Hostname   = config.get("mailConfig","Hostname")

Mailbox    = 'INBOX'
CmdSubject = '"get wr"'

list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

def parse_list_response(line):
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

try:
    if DEBUG:
        print "called at: ",strftime("%d-%m-%Y %H:%M:%S", localtime())
        
    m = imaplib.IMAP4_SSL(Hostname)
    m.login(Username, Password)

    typ, mailbox_data = m.list(Mailbox)
    
    for line in mailbox_data:
        flags, delimiter, mailbox_name = parse_list_response(line)
        m.select(mailbox_name, readonly=False)
        typ, [msg_ids] = m.search(None, '(FROM '+Sender+' SUBJECT '+CmdSubject+' UNSEEN)')
        # convert str -> list (to enable to sum up the no of found emails)
        msg_ids_list = msg_ids.split()

        if DEBUG:
            print "no of email ids with matched request criterias: ", len(msg_ids_list)
            for id in msg_ids_list:
                print "id = ",id

        # check if at least one email matches the request criteria
        if len(msg_ids_list) >= 1:
            #weather report was requested, send it...
            mailWeatherReport()
            if DEBUG:
                print "valid request detected: send weather report"
            #delete request message(s)
            msg_ids = ','.join(msg_ids.split(' ')) # comma sep. list of ids needed
            if DEBUG:
                print "msg_ids =", msg_ids
            typ, response = m.store(msg_ids, '+FLAGS', r'(\Deleted)')
            if DEBUG:
                print "response = ", response
        else:
            if DEBUG:
                print "no valid email request detected"

finally:
    m.close()
    m.logout()
    if DEBUG:
        print "Logout"

