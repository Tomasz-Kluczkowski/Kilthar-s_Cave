"""Thank you for the subscription to OpenWeatherMap Free service!


Dear Customer,
Your account and API key are activated for operating with OpenWeatherMap Free weather services.
Endpoint for any API calls
api.openweathermap.org
Example of API call

api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=fa730d41d41ae83226a227a150d927ac

5 days 3 hours call:
api.openweathermap.org/data/2.5/forecast?q=London,us&mode=xml

16 days daily call:
api.openweathermap.org/data/2.5/forecast/daily?q=London&mode=xml&units=metric&cnt=7

API documentation
http://openweathermap.org/api


Contact our Helpdesk info@openweathermap.org for any technical issues.


	Please, always use your API keys as &APPID=fa730d41d41ae83226a227a150d927ac in any queries.
We will refuse calls without API key or unauthorized API key. Read more http://openweathermap.org/appid#use
"""

"""
Background
If you would like to know the basics of what an API is, check out this post by iamapizza. http://www.reddit.com/r/explainlikeimfive/comments/qowts/eli5_what_is_api/c3z9kok
Goal
Create a program that pulls data from OpenWeatherMap.org that prints out information about the current weather,
such as the high, the low, and the amount of rain for wherever you live. Depending on how skilled you are, you can actually do some neat stuff with this project.
Subgoals
Print out data for the next 5-7 days so you have a 5 day/week long forecast.
Print the data to another file that you can open up and view at, instead of viewing the information in the command line.
If you know html, write a file that you can print information to so that your project is more interesting. Here is an example of the results from what I threw together.
Tips
APIs that are in Json are essentially lists and dictionaries. Remember that to reference something in a list,
you must refer to it by what number element it is in the list, and to reference a key in a dictionary, you must refer to it by it's name.
Don't like Celsius? Add &units=imperial to the end of the URL of the API to receive your data in Fahrenheit.

"""

import requests
import os
import string
import datetime


def question():
    user_answer = ""
    while user_answer not in ["y", "yes", "n", "no"]:
        user_answer = input("Do you want to try again? ")
        if user_answer.lower() in ["y", "yes"]:
            _ = os.system("cls")
            return True
        elif user_answer.lower() in ["n", "no"]:
            return False
        else:
            # TODO: trying to use ANSI escape code to clear screen and add colors but it does not work
            _ = os.system("cls")
            continue

def clear_screen():
    _ = os.system("cls")

# here we get rid of unwanted accidentally typed characters
punctuation = string.punctuation
translator = str.maketrans('', '', string.punctuation)
time_conv = datetime.datetime.fromtimestamp

w_d = {}
response = {}
api_key = "fa730d41d41ae83226a227a150d927ac"
base_url = "http://api.openweathermap.org/data/2.5/{0}?q={1}&units=metric&APPID="
forecast_type = None

# file_handle = open("weather_dict.txt", "w")
while not response:
    clear_screen()
    # TODO: MAIN MENU - CURRENT, DAILY, 5 DAY FORECAST. UNIT SELECTION (METRIC, STANDARD, IMPERIAL).
    # TODO: TEMP ETC. PLOTTING FROM MATPLOTLIB
    while forecast_type not in ["c", "d", "f"]:
        clear_screen()
        print("MAIN MENU")
        forecast_type = input("Please select forecast type. Press  c for current,"
                              " d for 5 days 3 hours report, f for 16 days daily forecast: ")

    if forecast_type == "c":
        forecast_type = "weather"
    elif forecast_type == "d":
        forecast_type = "forecast"
    else:
        forecast_type = "forecast/daily"

    location = input("Please enter location: ")
    location = location.translate(translator)

    try:
        response = requests.get(base_url.format(forecast_type, location) + api_key)
    except requests.exceptions.ConnectionError:
        print("Unable to establish connection. Please connect to the internet")
        if question():
            continue
        else:
            break

    w_d = response.json()
    if w_d["cod"] != 200:
        print("Error: {0}".format(w_d["cod"]), w_d["message"], "\n")
        if question():
            continue
        else:
            break
    print()
    print("Weather report for: {0}, {1}, lon: {2}, lat: {3}\n".
          format(w_d["name"], w_d["sys"]["country"],
                 w_d["coord"]["lon"], w_d["coord"]["lat"]))

    print("Weather type: {0}, {1}".format(w_d["weather"][0]["main"].lower(), w_d["weather"][0]["description"]))
    print("Cloud coverage: {0}%".format(w_d["clouds"]["all"]))
    print("Current temperature: {0} degC".format(w_d["main"]["temp"]))
    print("Current minimum temperature: {0} degC".format(w_d["main"]['temp_min']))
    print("Current maximum temperature: {0} degC".format(w_d["main"]['temp_max']))
    print("Pressure: {0} hPa".format(w_d["main"]["pressure"]))
    print("Humidity: {0}%".format(w_d["main"]["humidity"]))
    print("Visibility: {0} m".format(w_d["visibility"]))
    print()
    print("Wind speed: {0} m/s".format(w_d["wind"]["speed"]))
    print("Wind direction: {0} deg".format(w_d["wind"]["deg"]))
    print()
    print("Sunrise at: {0}".format(time_conv(w_d["sys"]["sunrise"]).strftime("%H:%M")))
    print("Sunset at: {0}".format(time_conv(w_d["sys"]["sunset"]).strftime("%H:%M")))

    print()
    # for (key, value) in w_d.items():
    #     print("{0} {1}".format(key, value))
    #     # file_handle.writelines()
