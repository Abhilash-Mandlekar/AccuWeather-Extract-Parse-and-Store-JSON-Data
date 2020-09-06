# AccuWeather-Reston

This small project is intended to collect the data of weather for a specific location say Reston and store it in json file.  It uses the AccuWeather API to get the weather data. It can forecast the data for next 5 days or can get the current weather data of that location.

## Build Environment:

This project is built on python version 3.8.2

The librabries used has the follwing versions:

requests 2.22.0

pytest 6.0.1

ujson 3.1.0

Please run the requirements.txt to install the above dependancies as follows:

#### pip install -r requirements.txt 


## Run:

Use either python or python3 command to run the weather.py file. 

The following command will forcast the weather data for next five days.

#### e.g. python3 weather.py

We can specify the postal code as command line argument to get the forecast of that postal code.

#### e.g. python3 weather.py --p 20190

We can optionally provide the command line argument to get the current weather of Reston.

#### e.g. python3 weather.py --c curr

We can also specify the outfile name through command line.

#### e.g. python3 weather.py --p 20190 --o reston_weather.json

The program can run with all the arguments giving the current weather of postal code and outputting the json of given name.

#### e.g. python3 weather.py --c curr --p 20190 --o reston_curr_weather.json


We can optionally provide the command line argument to get the current weather of Reston.

#### e.g. python3 weather.py --c curr

The file test.py contains the test cases that tests the weather.py.

Note: This takes the input as json file in one of the test case. The path of the file may needs to be updated.

#### e.g. python3 test.py

#### Note: Samples of raw data and processed data can be found in "Sample" folder.
