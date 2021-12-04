import json
from urllib3 import *
import sys
import math

#load weather data for chosen city
def loadData(city):
    #instantiating url manager
    manager = PoolManager(num_pools=1)
    #reading in raw data from api for chosen city
    httpsData = manager.request("GET", "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=cd6ab6e6294be26428ea871d641b75c6")
    #converting raw data to python dictionary
    data = json.loads(httpsData.data.decode('utf-8'))
    #return result
    return data

#apply humidity to temperature using Canadian humidex formula
def applyHumidity(temperature, humidity):
    dewpoint = (humidity/100)**(1/8) * (112 + (0.9*temperature)) + (0.1 * temperature) - 112
    adjustment = 0.5555 * (6.11 * math.exp(5417.753 * ((1/273.15) - (1/dewpoint))) - 10)
    return temperature + adjustment - 273.15

#print results of weather query
def printResults(data):
    glasscap ='\033[1;37;40m---'
    bulbedge = '\033[1;37;40m -' + '\033[1;31;40m++++++' + '\033[1;37;40m-'
    bulbmid = '\033[1;37;40m-' + '\033[1;31;40m++++++++' + '\033[1;37;40m'
    
    #determine how much to fill the thermometer
    #   empty thermometer: <= -30.15C
    #   full thermometer: <= 69.85C
    try:
        temp = data['main']['temp']
    except KeyError:
        print('City not found in database')
        return 1

    for i in range(0, 10):
        bulbedge += '\033[1;37;40m---'
        if temp > 243:
            bulbmid += '\033[1;31;40m+++'
            temp -= 10
        else:
            bulbmid += '   '
    
    #capping thermometer end
    bulbmid += '\033[1;37;40m-'

    #printing thermometer
    print('  ' + glasscap + glasscap)
    print(bulbedge)
    print(bulbmid)
    print(bulbedge)
    print('  ' + glasscap + glasscap)

    #outputting useful data
    print('The weather in ' + data['name'] + ', ' + data['sys']['country'] + ' today is: ' + data['weather'][0]['description'])
    print('high temp: \t%.2fC' % (data['main']['temp_max'] - 273.15))
    print('low temp: \t%.2fC' % (data['main']['temp_min'] - 273.15))
    print('rel humidity: \t%.0f' % data['main']['humidity'] + '%')
    print('humidex temp: \t%.2fC' % applyHumidity(data['main']['temp'], data['main']['humidity']))

#main:
def main():
    #default city is Toronto
    city = "Toronto"
    if(len(sys.argv) > 1):
        city = sys.argv[1]

    data = loadData(city)
    printResults(data)


#load main function
if __name__ == "__main__":
    main()
