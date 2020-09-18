import pytest
import ujson
import time
from weather import AccuWeatherReston, BadRequestException

    
def test_current_weather_data():
    """ tests the current weather data and json validation """
    j = AccuWeatherReston(postal_code = "20190", outfile_name = "test.json")
    assert j is not None
    
    curr_day_data = j.currData()
    
    j.cleanAndStoreCurrWeatherData(curr_day_data)
    
    with open("test.json", 'r') as output:
        jobj = ujson.load(output)
        item = jobj['CurrentWeather']
        
        assert 'LocalObservationDateTime' in item[0]
        assert 'Temperature' in item[0]
        assert 'WeatherText' in item[0]
    output.close()

    
def test_five_day_weather_data():
    """ tests the next five days weather data and json validation """
    j = AccuWeatherReston(postal_code = "20190", outfile_name = "test.json")
    assert j is not None
    
    five_day_data = j.nextFiveDayData() 
    
    j.cleanAndStoreDataFiveDay(five_day_data)
    
    with open("test.json", 'r') as output:
        jobj = ujson.load(output)
        for item in jobj['DailyForecasts']:
            assert 'Date' in item
            assert 'Temperature' in item
            assert 'Day' in item
            assert 'Night' in item
    output.close()
 

def test_bad_postal_code():
    with pytest.raises(BadRequestException):
        j = AccuWeatherReston(postal_code = "", outfile_name = "test.json")
