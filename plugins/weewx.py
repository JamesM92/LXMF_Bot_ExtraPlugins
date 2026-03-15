##############################
#!/usr/bin/python3
import sqlite3
from time import strftime, localtime
import math
from commands import register


##########
#variables
##########
database = '/var/lib/weewx/weewx.sdb'
data_points = [
  'dateTime', 
  'usUnits', 
  'interval', 
  'appTemp', 
  'cloudbase', 
  'dewpoint', 
  'heatindex', 
  'humidex', 
  'lightning_distance', 
  'lightning_strike_count', 
  'maxSolarRad', 
  'outHumidity', 
  'outTemp', 
  'rain', 
  'rainRate', 
  'windchill', 
  'windGust', 
  'windrun', 
  'windSpeed',
  'windDir'
  ]




@register(
    "weather",
    "current weather",
    category="weewx",
    cooldown=300
)
def weather(args):

    responsetext = ""

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        sql_query = f'SELECT {", ".join(data_points)} FROM archive ORDER BY dateTime DESC LIMIT 1'
        cur.execute(sql_query)
        data = cur.fetchone()
        conn.close()
    except Exception:
        data = None

    if not data:
        return "Weather data unavailable."

    responsetext += "Current Conditions\n"

    try:
        update = strftime('%Y-%m-%d %H:%M:%S', localtime(data[0]))
        responsetext += f"\tLast Updated: {update}\n"
    except:
        responsetext += "\tLast Updated: NA\n"

    responsetext += "Heat and Humidity\n"
    responsetext += f"\tTemperature:   \t{data[12]:.2f}°F\n"
    responsetext += f"\tHumidity:      \t\t{data[11]:.0f}%RH\n"
    responsetext += f"\tHeat Index:  \t\t{data[6]:.2f}°F\n"
    responsetext += f"\tDew Point:   \t\t{data[5]:.2f}°F\n"

    responsetext += "Wind and Rain\n"
    responsetext += f"\tWind Speed:  \t\t{data[18]:.2f} MPH\n"

    # Wind direction
    directions = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
                  'S','SSW','SW','WSW','W','WNW','NW','NNW']

    try:
        if data[19] is not None:
            card = int((data[19] + 11.25) / 22.5) % 16
            responsetext += f"\tWind Dir:    \t\t\t{data[19]:.2f}° - {directions[card]}\n"
        else:
            responsetext += "\tWind Dir:    \t\t\tNA\n"
    except:
        responsetext += "\tWind Dir:    \t\t\tNA\n"

    responsetext += f"\tWind Chill:  \t\t\t{data[15]:.2f}°F\n"
    responsetext += f"\tRain:        \t\t\t{data[13]:.2f} IN\n"

    responsetext += "Clouds and Lightning\n"
    responsetext += f"\tCloud Base:  \t\t{data[4]:.2f} Ft\n"
    responsetext += "Lightning\n"
    responsetext += f"\tDistance:    \t\t\t{data[8]:.2f} Miles\n"
    responsetext += f"\tStrikes:       \t\t\t{data[9]:.0f}\n"

    return responsetext
