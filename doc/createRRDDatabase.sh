#!/bin/bash
# Create rrd database for weather measurement
#
# One average value for each quarter hour (step: 900 s = 15 min) of 2 * 8 + 5 sensors (Wettermast) + 2 sensors (BMP180)
#
# Average         1: 960 samples every 15 min (= 24*4*10) to store for 10 days 
# Average/Min/Max 2: 1 sample per day out of 96 (= 24*4) to store for 3600 days 
#
# TFN bugfix?: U instead 0.027 as max value for rains9
# TFN add psea and temps10 from airpressure sensor; xfiles factor 0.7 instead of 0.5 for rra

rrdtool create weather3.rrd --step 900 \
DS:temps1:GAUGE:1200:-40:50 \
DS:temps2:GAUGE:1200:-40:50 \
DS:temps3:GAUGE:1200:-40:50 \
DS:temps4:GAUGE:1200:-40:50 \
DS:temps5:GAUGE:1200:-40:50 \
DS:temps6:GAUGE:1200:-40:50 \
DS:temps7:GAUGE:1200:-40:50 \
DS:temps8:GAUGE:1200:-40:50 \
DS:hums1:GAUGE:1200:0:100 \
DS:hums2:GAUGE:1200:0:100 \
DS:hums3:GAUGE:1200:0:100 \
DS:hums4:GAUGE:1200:0:100 \
DS:hums5:GAUGE:1200:0:100 \
DS:hums6:GAUGE:1200:0:100 \
DS:hums7:GAUGE:1200:0:100 \
DS:hums8:GAUGE:1200:0:100 \
DS:temps9:GAUGE:1200:-40:50 \
DS:hums9:GAUGE:1200:0:100 \
DS:winds9:GAUGE:1200:0:200 \
DS:rains9:DERIVE:1200:0:U \
DS:israins9:GAUGE:1200:0:1 \
DS:temps10:GAUGE:1200:-40:50 \
DS:psea:GAUGE:1200:900:1100 \
RRA:AVERAGE:0.5:1:960 \
RRA:MIN:0.5:96:3600 \
RRA:MAX:0.5:96:3600 \
RRA:AVERAGE:0.5:96:3600
