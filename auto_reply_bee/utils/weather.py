# coding=utf-8
"""
Get weather infomation from a specified city.
"""
import requests

__all__ = ['get_rttodayweather']



def get_rttodayweather(cityname, country = 'uk'):
    """
    Get weather infomation from a specified city.
    Weather information provided by http://api.openweathermap.org/data/2.5/weather?parameters
    :param cityname:str The name of the city.
    :param country:str The name of the country, default to uk.
    :return:str Weather
    """
    print('Getting info of {} weather...'.format(cityname))
    weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q={},{}&APPID=5f78783fda025d43069d735b090743fa'.format(cityname, country)).json()
    main_weather = weather['weather'][0]['description']
    visibility = weather['visibility']
    wind_speed = weather['wind']['speed']
    humidity = weather['main']['humidity']
    pressure = weather['main']['pressure']
    return 'Weather of {} today:\nweather: {}\nvisibility: {}\nwind speed: {}\nhumidity: {}\npressure: {}\n'.format(cityname, main_weather, visibility, wind_speed, humidity, pressure)





if __name__ == '__main__':
    # cityname = 'Manchester'
    # weather = get_today_weather(cityname)
    # print(weather)
    pass
    
