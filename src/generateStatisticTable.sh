#!/bin/bash

# TFN 180417 passing fileName and MailMode parameter to python script to generate html file according to usage
# TFN 180317 calling dumpStatistics_v4 due to new table format in html
# TFN 260217 calling dumpStatistics_v3 due to new table format
# TFN 190117 ***neu***

# set WESTA_ACTIV_SRC variable (to get appropiate prod/dev sources)
source /etc/environment

# html Datentabelle aus SQL-DB erzeugen
# 1. parameter: filename to be generated
# 2. parameter: mode for generating html file

python $WESTA_ACTIV_SRC'dumpStatistics.py' $1 $2

if [ "$2" == "MailModeActiv" ]
	then
		#echo "Mail Mode aktiv"
		# move generated file to reports for being mailed
		sudo mv ./$1 /var/www/html/reports/
	else
		#echo "Mail Mode nicht aktiv"
		# move generated file to web server for being displayed
		sudo mv ./$1 /var/www/html/html/
fi



