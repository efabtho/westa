#!/bin/bash

# TFN 180317 v2 calling dumpStatistics_v4 due to new table format in html
# TFN 260217 v2 calling dumpStatistics_v3 due to new table format
# TFN 190117 v1 ***neu***

# set WESTA_ACTIV_SRC variable (to get appropiate prod/dev sources)
source /etc/environment

# html Datentabelle aus SQL-DB erzeugen
#echo calling python $WESTA_ACTIV_SRC'dumpStatistics.py'
python $WESTA_ACTIV_SRC'dumpStatistics.py'

# generated File rüberschieben auf Web-Server
sudo mv ./min-max-values_generated.html /var/www/html/html/

