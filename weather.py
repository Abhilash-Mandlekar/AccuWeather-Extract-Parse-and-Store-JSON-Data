import os
import sys
import argparse
import requests
import ujson

API_KEY = "Rp2qWkX61A3iqGmjJrKMmunR8xgnzTpM"  #"94lw2xFLTQ5cdPGRH2OuGii2G2zp4NwN"
#LOCATION_KEY = "341249"
OUTFILE_NAME = "reston_weather.json"
POSTAL_CODE = "20190"

class AccuWeatherReston:
    """ Gets the weather data for reston using AccuWeather API. The location key for Reston is 341249 """
    
    def __init__(self, key=API_KEY, postal_code=POSTAL_CODE, outfile_name=OUTFILE_NAME):
        self.key = key
        self.postal_code = postal_code
        self.outfile_name = outfile_name
        url = f"http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey=Rp2qWkX61A3iqGmjJrKMmunR8xgnzTpM&q={self.postal_code}&language=en-us&details=false"
        response = requests.get(url)
        
        # check if the response is OK else raise an exception
        if response.status_code == 200:
            raw_data = ujson.loads(response.text)
            self.location_key = raw_data[0]["Key"]
            
        else:
            """ bad request, 401 , 404 server errors"""
            print("Bad request")
            raise raise_for_status()
            
       
    def get(self, url):
        """ calls the API for specified URL """
        raw_data = ""
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                raw_data = ujson.loads(response.text)
                                
        except requests.ConnectionError:
            print("ConnectionError")
            
        except requests.exceptions.HTTPError as err:
            print("")
        
        return raw_data
                
    
    def nextFiveDayData(self):
        """ Calls the Accu weather API to get the raw weather data for last 5 days"""

        return self.get(f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{self.location_key}?apikey={self.key}&amp;details=false")
            

    def currData(self):
        """ Calls the Accu weather API to get the current conditions of Reston """
        
        return self.get(f"http://dataservice.accuweather.com/currentconditions/v1/{self.location_key}?apikey={self.key}&amp;details=false")
        
        
    def cleanDataFiveDay(self, raw_data):
        """ cleans the data for next 5 days and only takes important fields from json """
        
        cleaned_data = {'DailyForecasts': []}
        
        for item in raw_data["DailyForecasts"]:
            #print(item)
            json_data = {}
            # clean date
            date = ''.join(item['Date'].split("T",1)[0])
            json_data['Date'] = date
            
            json_data['Temperature'] = item['Temperature']
            json_data['Day'] = item['Day']
            json_data['Night'] = item['Night']
            
            temp = cleaned_data['DailyForecasts']
            temp.append(json_data)
            
            
        self.jsonDump(cleaned_data)
    
    
    def cleanCurrWeatherData(self, raw_data):
        """ cleans the data for next 5 days and only takes important fields from json """
        
        cleaned_data = {'CurrentWeather': []}
        
        for item in raw_data:
            #print(item)
            json_data = {}
            json_data['LocalObservationDateTime'] = item['LocalObservationDateTime']
            json_data['Temperature'] = item['Temperature']
            json_data['WeatherText'] = item['WeatherText']
            
            temp = cleaned_data['CurrentWeather']
            temp.append(json_data)
            
            
        self.jsonDump(cleaned_data)
        
        
    
    def jsonDump(self, json_data):
        """ opens/creates the file in write mode and dumps json data to it """
        ujson.dumps(json_data)
        with open(self.outfile_name, 'w') as outfile:
            ujson.dump(json_data, outfile)
        #print("File created")
    
    


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Calls API for weather data')
    parser.add_argument("--c", 
        help="pass 'curr' for current weather or pass 'fivedays' for last five days weather")
        
    args = parser.parse_args()
    #print(args.c)
    if (args.c == 'curr'):
        j = AccuWeatherReston()
        curr_day_data = j.currData()
        print(curr_day_data)    
        j.cleanCurrWeatherData(curr_day_data)
        
    else:
        j = AccuWeatherReston()
        five_day_data = j.nextFiveDayData()
        print(five_day_data)    
        j.cleanDataFiveDay(five_day_data)