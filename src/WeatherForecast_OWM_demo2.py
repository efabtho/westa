
import pyowm
import json

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
 
#Create String to Print
strMsg = 'Hildesheim: ' + detailed_status.title() + \
         ' (weitere Aussichten: ' + detailed_status_later.title() + ') von ' + \
         str(w.get_temperature('celsius')['temp_min']) + '°C bis ' + \
         str(w.get_temperature('celsius')['temp_max']) + '°C, ' + \
         str(decoded_w['humidity']) + '% Luftfeuchtigkeit; ' + \
         str(decoded_w['clouds']) + '% Bewölkung'
print(strMsg)
