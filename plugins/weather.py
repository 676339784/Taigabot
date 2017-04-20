from util import hook, http, web, database
<<<<<<< HEAD


# def get_weather(location):
#     """uses the yahoo weather API to get weather information for a location"""

#     query = "SELECT * FROM weather.bylocation WHERE location=@location LIMIT 1"
#     result = web.query(query, {"location": location})

#     data = result.rows[0]["rss"]["channel"]

#     # wind conversions
#     data['wind']['chill_c'] = int(round((int(data['wind']['chill']) - 32) / 1.8, 0))
#     try: data['wind']['speed_kph'] = int(round(float(data['wind']['speed']) * 1.609344))
#     except: data['wind']['speed_kph'] = 0

#     # textual wind direction
#     direction = data['wind']['direction']
#     if direction >= 0 and direction < 45:
#         data['wind']['text'] = 'N'
#     elif direction >= 45 and direction < 90:
#         data['wind']['text'] = 'NE'
#     elif direction >= 90 and direction < 135:
#         data['wind']['text'] = 'E'
#     elif direction >= 135 and direction < 180:
#         data['wind']['text'] = 'SE'
#     elif direction >= 180 and direction < 225:
#         data['wind']['text'] = 'S'
#     elif direction >= 225 and direction < 270:
#         data['wind']['text'] = 'SW'
#     elif direction >= 270 and direction < 315:
#         data['wind']['text'] = 'W'
#     elif direction >= 315 and direction < 360:
#         data['wind']['text'] = 'NW'
#     else:
#         data['wind']['text'] = 'N'

#     # visibility and pressure conversions
#     try:
#         data['atmosphere']['visibility_km'] = int(round(float(data['atmosphere']['visibility']) * 1.609344))
#         data['atmosphere']['visibility_km'] = str(round((float(data['atmosphere']['visibility']) * 33.8637526), 2))
#     except ValueError: pass

#     # textual value for air pressure
#     rising = data['atmosphere']['rising']
#     if rising == 0:
#         data['atmosphere']['tendancy'] = 'steady'
#     elif rising == 1:
#         data['atmosphere']['tendancy'] = 'rising'
#     elif rising == 2:
#         data['atmosphere']['tendancy'] = 'falling'

#     # current conditions
#     data['item']['condition']['temp_c'] = \
#         int(round(((float(data['item']['condition']['temp']) - 32) / 9) * 5))

#     # forecasts
#     for i in data['item']['forecast']:
#         i['high_c'] = \
#         int(round(((float(i['high']) - 32) / 9) * 5))
#         i['low_c'] = \
#         int(round(((float(i['low']) - 32) / 9) * 5))

#     return data


# @hook.command('w', autohelp=False)
# @hook.command('we', autohelp=False)
# @hook.command(autohelp=False)
# def weather(inp, nick=None, reply=None, db=None, notice=None):
#     "weather | <location> [save] | <@ user> -- Gets weather data for <location>."
#     save = True

#     if '@' in inp:
#         save = False
#         nick = inp.split('@')[1].strip()
#         loc = database.get(db,'users','location','nick',nick)
#         if not loc: return "No location stored for {}.".format(nick.encode('ascii', 'ignore'))
#     else:
#         loc = database.get(db,'users','location','nick',nick)
#         if not inp:
#             if not loc:
#                 notice(weather.__doc__)
#                 return
#         else:
#             # if not loc: save = True
#             if " dontsave" in inp:
#                 inp = inp.replace(' dontsave','')
#                 save = False
#             loc = inp.replace(' ','_') #.split()[0]

#     location = http.quote_plus(loc)
#     # location = location.replace(',','').replace(' ','-')

#     # now, to get the actual weather
#     try:
#         data = get_weather('%s' % location)
#     except KeyError:
#         return "Could not get weather for that location."

#     if location and save: database.set(db,'users','location',location,'nick',nick)

#     # put all the stuff we want to use in a dictionary for easy formatting of the output
#     weather_data = {
#         "place": data['location']['city'],
#         "conditions": data['item']['condition']['text'],
#         "temp_f": data['item']['condition']['temp'],
#         "temp_c": data['item']['condition']['temp_c'],
#         "humidity": data['atmosphere']['humidity'],
#         "wind_kph": data['wind']['speed_kph'],
#         "wind_mph": data['wind']['speed'],
#         "wind_text": data['wind']['text'],
#         "forecast": data['item']['forecast'][0]['text'],
#         "high_f": data['item']['forecast'][0]['high'],
#         "high_c": data['item']['forecast'][0]['high_c'],
#         "low_f": data['item']['forecast'][0]['low'],
#         "low_c": data['item']['forecast'][0]['low_c'],
#         "_forecast": data['item']['forecast'][1]['text'],
#         "_high_f": data['item']['forecast'][1]['high'],
#         "_high_c": data['item']['forecast'][1]['high_c'],
#         "_low_f": data['item']['forecast'][1]['low'],
#         "_low_c": data['item']['forecast'][1]['low_c']
#     }

#     return "\x02{place}\x02 - \x02Current:\x02 {conditions}, {temp_f}F/{temp_c}C, Humidity: {humidity}%, " \
#         "Wind: {wind_kph}KPH/{wind_mph}MPH {wind_text}, \x02Today:\x02 {forecast}, " \
#         "High: {high_f}F/{high_c}C, Low: {low_f}F/{low_c}C. " \
#         "\x02Tomorrow:\x02 {_forecast}, High: {_high_f}F" \
#         "/{_high_c}C, Low: {_low_f}F/{_low_c}C.".format(**weather_data)




@hook.command('w', autohelp=False)
@hook.command('we', autohelp=False)
@hook.command(autohelp=False)
def weather(inp, bot=None, reply=None, db=None, nick=None, notice=None):
    """weather | <location> [dontsave] | <@ user> -- Gets weather data for <location>."""
    inp = ','.join(inp.replace(',', '').split())
    apikey = bot.config.get("api_keys", {}).get("openweathermap")
    save = True
=======
import json
import urllib

base_url = 'https://query.yahooapis.com/v1/public/yql?'
def query(query):
    url = base_url + urllib.urlencode(query)
    response = urllib.urlopen(url)
    data = response.read()
    return data

@hook.command('w', autohelp=False)
@hook.command('we', autohelp=False)
@hook.command(autohelp=False)
def weather(inp, nick=None, reply=None, db=None, notice=None):
    "weather | <location> [save] | <@ user> -- Gets weather data for <location>."
    save = False 
    
    if '@' in inp:
        save = False
        nick = inp.split('@')[1].strip()
        loc = database.get(db,'users','location','nick',nick)
        if not loc: return "No location stored for {}.".format(nick.encode('ascii', 'ignore'))
    else:
        loc = database.get(db,'users','location','nick',nick)
        if not inp:
            if not loc:
                notice(weather.__doc__)
                return
        else:
            # if not loc: save = True
            if " save" in inp: 
                inp = inp.replace(' save','')
                save = True 
            loc = inp.replace(' ','_') #.split()[0]

    location = http.quote_plus(loc)
    # location = location.replace(',','').replace(' ','-')

    # now, to get the actual weather
    try:

	    q ={
		'q': 'select title, units.temperature, item.forecast from weather.forecast where woeid in (select woeid from geo.places where text="'+ location+'") limit 1',
		 'format': 'json',
		 'env': 'store://datatables.org/alltableswithkeys'
		}

	    result = query(q)
	    data = json.loads(result)
	    weather = data["query"]["results"]["channel"]
	    average_F =  float((int(weather['item']['forecast']['high']) + int(weather['item']['forecast']['low']))/2)
	    average_C = round(float((average_F - 32) * (5.0/9.0)), 2)
    except KeyError:
        return "Could not get weather for that location."

    if location and save: database.set(db,'users','location',location,'nick',nick)

    # put all the stuff we want to use in a dictionary for easy formatting of the output
    weather_data = {
	'title': weather["title"].replace("Yahoo! Weather -", ""), 
	'current': weather['item']['forecast']['text'],
	'temp_f': average_F,
	'temp_c': average_C
    }
 
    reply("\x02{title}\x02 - \x02Current:\x02 {current}, {temp_f}F/{temp_c}C".format(**weather_data))

@hook.command(autohelp=False)
def save(inp, nick=None, reply=None, db=None, notice=None):
    "weather | <location> [save] | <@ user> -- Gets weather data for <location>."
    save = True
    loc = database.get(db,'users','location','nick',nick)
>>>>>>> infinuguu/master
    if '@' in inp:
        save = False
        nick = inp.split('@')[1].strip()
        loc = database.get(db,'users','location','nick',nick)
        if not loc: return "No location stored for {}.".format(nick.encode('ascii', 'ignore'))
    else:
        loc = database.get(db,'users','location','nick',nick)
        if not inp:
            if not loc:
                notice(weather.__doc__)
                return
<<<<<<< HEAD
            else:
                inp = loc
                save = False
        else:
            # if not loc: save = True
            if " dontsave" in inp:
                inp = inp.replace(' dontsave','')
                save = False

    if inp and save:
        database.set(db,'users','location',inp,'nick',nick)
    try:
        if int(inp) or int(inp.split(',')[0]):
            url = 'http://api.openweathermap.org/data/2.5/weather?zip={}&appid={}'
        else:
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    except:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    json = http.get_json(url.format(inp, apikey))
    place = json['name'] + ', ' + json['sys']['country']
    conditions = json['weather'][0]['description']
    temp_f = (json['main']['temp'] - 273.15) * 1.8000 + 32.00
    temp_c = (json['main']['temp'] - 273.15) * 1
    humidity = json['main']['humidity']
    wind_kph = json['wind']['speed'] * 3.60
    wind_mph = json['wind']['speed'] * 2.24
    response = ('\x02{place}\x02 - \x02Current:\x02 {conditions}, {temp_f}F/'
                '{temp_c}C, Humidity: {humidity}%, Wind: {wind_kph}KPH/'
                '{wind_mph}MPH')
    weather_data = {
        'place': place,
        'conditions': conditions,
        'temp_f': temp_f,
        'temp_c': temp_c,
        'humidity': humidity,
        'wind_kph': wind_kph,
        'wind_mph': wind_mph
    }
    reply(response.format(**weather_data))
=======
        else:
            # if not loc: save = True
            if " dontsave" in inp: 
                inp = inp.replace(' dontsave','')
                save = False
            loc = inp.replace(' ','_') #.split()[0]

    if location and save: database.set(db,'users','location',location,'nick',nick)
>>>>>>> infinuguu/master
