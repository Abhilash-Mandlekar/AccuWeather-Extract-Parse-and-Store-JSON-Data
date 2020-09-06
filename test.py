import unittest
import ujson
import time
from weather import AccuWeatherReston

class TestAccuWeatherReston(unittest.TestCase):

    def setUp(self) -> None:
        """ setup the testing environment """
        self.path = "reston_weather.json"
    
    def test_readjson(self):
        """ Tests the json file for last five day data """
        start = time.time()
        with open(self.path, 'r') as infile:
            jobj = ujson.load(infile)
            for item in jobj['DailyForecasts']:
                print(item['Date'])
                print(item['Temperature'])
                print(item['Day'])
                print(item['Night'])
        print("Total time taken to read and process json:", time.time() - start)    
            
    
if __name__ == '__main__':
    unittest.main()