import os
import sys
import argparse
import requests
import ujson

API_KEY =  {#Use your own API KEY}
OUTFILE_NAME = "reston_weather.json"
POSTAL_CODE = "20190"


class BadRequestException(Exception):
    
    def __init__(self):
        super().__init__("Bad request")

class AccuWeatherReston:
    """ Gets the weather data for reston using AccuWeather API. The location key for Reston is 341249 """
    
    def __init__(self, key=API_KEY, postal_code=POSTAL_CODE, outfile_name=OUTFILE_NAME):
        self.key = key
        self.postal_code = postal_code
        self.outfile_name = outfile_name
        url = f"http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey={self.key}&q={self.postal_code}&language=en-us&details=false"
        response = requests.get(url)
        # check if the response is OK else raise an exception
        if response.status_code == 200:
            raw_data = ujson.loads(response.text)
            if len(raw_data) == 0:
                raise BadRequestException()
            self.location_key = raw_data[0]["Key"]
            
        else:
            print("*****Status code", response.status_code)
            """ bad request, 401 , 404 server errors"""
            raise BadRequestException()
            
       
    def get(self, url):
        """ calls the API for specified URL """
        raw_data = ""
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                raw_data = ujson.loads(response.text)
                                
        except requests.ConnectionError:
            raise BadRequestException()
            
        except requests.exceptions.HTTPError as err:
            raise BadRequestException()
        
        return raw_data
                
    
    def nextFiveDayData(self):
        """ Calls the Accu weather API to get the raw weather data for next 5 days"""

        return self.get(f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{self.location_key}?apikey={self.key}&amp;details=false")
            

    def currData(self):
        """ Calls the Accu weather API to get the current conditions of Reston """
        
        return self.get(f"http://dataservice.accuweather.com/currentconditions/v1/{self.location_key}?apikey={self.key}&amp;details=false")
        
        
    def cleanAndStoreDataFiveDay(self, raw_data):
        """ cleans and stores the data for next 5 days and only takes important fields  """
        
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
    
    
    def cleanAndStoreCurrWeatherData(self, raw_data):
        """ extracts and stores important fields from current weather """
        
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
        outfile.close()
        print("File created")
    
    


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Optional arguments')
    
    parser.add_argument("--c", type = str,
        help="pass 'curr' for current weather ")
        
    parser.add_argument("--p", type = int,
        help="pass postal code (integer) to get the weather data for specified postal code",
        default = "20190")
    
    parser.add_argument("--o", type = str,
        help="pass output file name for json e.g. reston_weather.json",
        default = "reston_weather.json")
        
    args = parser.parse_args()
    #print(args.c)
    if (args.c == 'curr'):
        j = AccuWeatherReston(postal_code = args.p, outfile_name = args.o)
        curr_day_data = j.currData()
        print(curr_day_data)    
        j.cleanAndStoreCurrWeatherData(curr_day_data)
    
    else:
        j = AccuWeatherReston(postal_code = args.p, outfile_name = args.o)
        five_day_data = j.nextFiveDayData()
        print(five_day_data)    
        j.cleanAndStoreDataFiveDay(five_day_data)
