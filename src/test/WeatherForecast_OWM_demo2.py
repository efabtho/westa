
import pyowm
import json
import datetime
from time import gmtime

API_Key       = 'd8e69011a4a1450808fef780c686b3cf'
owm           = pyowm.OWM(API_Key)
#Documentation is at https://pyowm.readthedocs.org/en/latest/pyowm.html
 
#establish time constant
in3hours = pyowm.timeutils.next_three_hours()
 
#Retreive daily forecast
forecast = owm.daily_forecast('Hildesheim, Germany')
 
#Retrieve forecast at location in 3 hours
latertoday = forecast.get_weather_at(in3hours)
decoded_later = json.loads(latertoday.to_JSON()) #its easier to load it into JSON and decode it!
detailed_status_later = decoded_later['detailed_status'] #detailed status in 3 hours
 
# Search for current weather
observation = owm.weather_at_place('Hildesheim, Germany')
w = observation.get_weather()
decoded_w = json.loads(w.to_JSON())
detailed_status = decoded_w['detailed_status']

# sunrise time
if gmtime()[8] == 0: # 0= keine Sommerzeit aktiv
    sunrise = (datetime.datetime.strptime(w.get_sunrise_time('iso'),"%Y-%m-%d %H:%M:%S+00") + \
               datetime.timedelta(hours=1)).strftime("%H:%M")     
else:
    sunrise = (datetime.datetime.strptime(w.get_sunrise_time('iso'),"%Y-%m-%d %H:%M:%S+00") + \
               datetime.timedelta(hours=2)).strftime("%H:%M")      

# sunset time
if gmtime()[8] == 0: # 0= keine Sommerzeit aktiv
    sunset = (datetime.datetime.strptime(w.get_sunset_time('iso'),"%Y-%m-%d %H:%M:%S+00") + \
              datetime.timedelta(hours=1)).strftime("%H:%M")     
else:
    sunset = (datetime.datetime.strptime(w.get_sunset_time('iso'),"%Y-%m-%d %H:%M:%S+00") + \
              datetime.timedelta(hours=2)).strftime("%H:%M")     
 
#Create String to Print
strMsg = 'Die Wettervorhersage für Hildesheim (von OWM):\n' + detailed_status.title() + \
         ' (weitere Aussichten: ' + detailed_status_later.title() + ') von ' + \
         str(w.get_temperature('celsius')['temp_min']) + '°C bis ' + \
         str(w.get_temperature('celsius')['temp_max']) + '°C; ' + \
         str(decoded_w['clouds']) + '% Bewölkung; ' + \
         "Sonnenaufgang um " + str(sunrise) + "h, " + \
         "Sonnenuntergang um " + str(sunset) + "h"
print(strMsg)

print("Wir haben Sommerzeit:" + str(gmtime()[8]))

#         str(decoded_w['humidity']) + '% Luftfeuchtigkeit; ' +
