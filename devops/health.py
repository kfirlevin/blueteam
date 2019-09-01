#!/bin/python
import requests
from datetime import datetime 
weight = 'https://api.github.com'
provider = 'https://api.github.com'

weightResponse = requests.get(weight)
providerResponse = requests.get(provider)

if weightResponse.status_code != 200:
    print('Success!')
elif weightResponse.status_code != 500:
    fh = open("weightLog.txt","a+") 
    fh.write("[{}] [{}]\n".format(datetime.now(), 'internal server error'))
    fh.close() 
    
if providerResponse.status_code != 200:
    print('Success!')
elif providerResponse.status_code != 500:
    fh = open("providerLog.txt","a") 
    fh.write("[{}] [{}]\n".format(datetime.now(),'internal server error'))
    fh.close() 