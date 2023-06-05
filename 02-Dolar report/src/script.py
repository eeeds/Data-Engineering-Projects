import sys
sys.path.append('../credentials/') 
from credentials import DolarCredentials
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



def get_dolar(url:str = 'https://dolar.melizeche.com/api/1.0/'):
    r = requests.get(url)
    dolar_value = r.json()['dolarpy']['bcp']['compra']
    hour = r.json()['updated']

    return dolar_value, hour

def send_message(dolar_value, hour):
    credentials = DolarCredentials()
    account_sid = credentials.TWILIO_ACCOUNT_SID
    auth_token = credentials.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=f"Hi, this is your dolar report for now. It's currently {dolar_value} and it was updated at {hour}",
                        from_=credentials.PHONE_NUMBER,
                        to='+595 982 355439'
                    )
    return message.sid


if __name__=='__main__':
    dolar_value, hour = get_dolar()

    dolar_dict = {'dolar_value':dolar_value, 'hour':hour}
    df = pd.DataFrame(dict, index = [0])

    ## Send message
    send_message(dolar_value, hour)