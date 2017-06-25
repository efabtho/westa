
import pyowm

API_Key       = 'd8e69011a4a1450808fef780c686b3cf'
owm           = pyowm.OWM(API_Key)
observation   = owm.weather_at_place("Hildesheim, Germany")
weatherObject = observation.get_weather()
wind          = weatherObject.get_wind()
clouds        = weatherObject.get_clouds()
temperature   = weatherObject.get_temperature('celsius')
tomorrow      = pyowm.timeutils.tomorrow()

# test forecasts
fc = owm.daily_forecast('Hildesheim, Germany', limit=3)
f  = fc.get_forecast()


print("gelieferte Wetterdaten: ", weatherObject)
print("Wind                  : ", wind)
print("Bewoelkung            : ", clouds)
print("Temperatur            : ", temperature)
print("Wetterprogn. Morgen   : ", tomorrow)
      
print ("Laenge f: ", len(f))

for weather in f:
    print(weather.get_reference_time('iso'), weather.get_status())

print("will it rain in forecast? ", fc.will_have_rain())
