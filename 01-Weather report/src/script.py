import sys 
sys.path.append('./credentials/')
from credentials import WeatherCredentials
from twilio.rest import Client
from requests import Request, Session 
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import time 
import os 
import json 


import pandas as pd 
import requests 
from bs4 import BeautifulSoup
from tqdm import tqdm

from datetime import datetime



def get_forecast(response,i):
    date = response['forecast']['forecastday'][0]['date']
    hour = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condition = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    temp_c = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    will_it_rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    chance_of_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    return date, hour, condition, temp_c, will_it_rain, chance_of_rain
    
def send_sms_twilio(account_sid, auth_token, body, number='+15005550006', to = '+595 982 355 439'):
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                        body=body,
                        from_=number,
                        to=to
                    )
    return message.sid

def get_weather(api_key, city = 'Asunción'):
    api_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=no&alerts=no"
    response = requests.get(api_url)
    return response.json()


if __name__ =='__main__':

    data = []
    credentials = WeatherCredentials()
    api_key = credentials.get_weather_api()
    response = get_weather(api_key=api_key)

    
    for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour'])), colour='green'):

        data.append(get_forecast(response,i))
        time.sleep(0.1)
    
    df = pd.DataFrame(data, columns = ['Date', 'Hour', 'Condition', 'Temp', 'Will_it_rain', 'Chance_of_rain'])
    ## Looking for cases that have a chance_of_rain greater than 65
    df_rain = df[df['Chance_of_rain'] > 65]
    ## If df_rain is len=0, then create a row with data
    if len(df_rain) == 0:
        df_rain = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H"), 'No rain', 0, 0, 0]], columns = ['Date', 'Hour', 'Condition', 'Temp', 'Will_it_rain', 'Chance_of_rain'])
    print(df_rain)
    ## Send sms
    message_template = "Hi, this is your weather report for today. It is currently {temp_c} degrees and {condition}. There is a {chance_of_rain}% chance of rain. Have a nice day!"
    account_sid = credentials.get_twilio_account_sid()
    auth_token = credentials.get_twilio_auth_token()
    send_sms_twilio(account_sid, auth_token, body = message_template.format(temp_c=df_rain['Temp'].values[0],
                            condition=df_rain['Condition'].values[0],
                            chance_of_rain=df_rain['Chance_of_rain'].values[0]))

    