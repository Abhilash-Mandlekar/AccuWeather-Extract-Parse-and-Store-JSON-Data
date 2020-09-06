AccuWeather 
This small project is intended to collect the data of weather for a specific location (Reston) and store it in json file. 
It uses the AccuWeather API to get the weather data. It can get the data from last 5 days or can get the current weather data of the location.

Build Environment:

This project is buit on python version 3.8.2

The librabries used has the follwing versions:
requests 2.22.0
pytest 6.0.1
ujson 3.1.0

Please run the requirements.txt to install the above dependancies as follows:

pip install -r requirements.txt 


Run:

Use either python or python3 command to run the weather.py file. This will get the data for last five days.
e.g. python3 weather.py

We can optionally provide the command line argument to get the current weather of Reston.
e.g. python3 weather.py --c curr

The file test.py contains the test cases that tests the weather.py.
Note: This takes the input as json file in one of the test case. The path of the file may needs to be updated. 
e.g. python3 test.py

Samples of raw data and processed data can be found in sample data folder.
 