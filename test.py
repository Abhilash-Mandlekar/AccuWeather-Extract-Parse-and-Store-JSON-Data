import pytest
import ujson
import time
from weather import AccuWeatherReston, BadRequestException

"""
class TestAccuWeatherReston(unittest.TestCase):

    def setUp(self) -> None:
        
        self.path = "reston_weather.json"
        self
    def test_readjson(self):
        
        start = time.time()
        with open(self.path, 'r') as infile:
            jobj = ujson.load(infile)
            for item in jobj['DailyForecasts']:
                print(item['Date'])
                print(item['Temperature'])
                print(item['Day'])
                print(item['Night'])
        print("Total time taken to read and process json:", time.time() - start)    
            
    def test_A():
        
if __name__ == '__main__':
    unittest.main()
    """
    
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
        
def test_bad_postal_code():
    with pytest.raises(BadRequestException):
        j = AccuWeatherReston(postal_code = "", outfile_name = "test.json")
