#!/bin/python
from requests.exceptions import HTTPError
from datetime import datetime 
import requests
"""
================================INFO==================================
flag2: true if all api's working, false if one api or more not working

getApi: func that send GET requests and check response
postApi: func that send POST requests and check response
putApi: func that send PUT requests and check response

getProvider: func that checking all provider GET api's
postProvider: func that checking all provider POST api's
getWeight: func that checking all Weight GET api's
postWeight: func that checking all Weight POST api's
fh: Write to errorLog.txt

======================================================================
"""
flag2 = True
url = 'http://blue.develeap.com:'
portProvider = '8080/'
portWeight = '8090/'
def getApi(port , api):
    fullPath = url + port + api
    fh = open("errorLog.txt","a")
    try:
        response = requests.get(fullPath) 
        response.raise_for_status()
    except HTTPError as http_err:
        #if api not found
        if response.status_code == 404:
            fh.write("{}\n".format(http_err))
            fh.close()
            return True 
        fh.write("{}\n".format(http_err))
        fh.close()
        return False
    except Exception as err:
        fh.write("{}\n".format(err))
        fh.close()
        return False
    else:
        fh.write('{} test sccess!\n'.format(fullPath))
        return True

def postApi(port , api):
    fullPath = url + port + api
    fh = open("errorLog.txt","a+")
    try:
        response = requests.post(fullPath , data={'key':'value'}) 
        response.raise_for_status()
    except HTTPError as http_err:
        #if api not found
        if response.status_code == 404:
            fh.write(fh.write("{}\n".format(http_err)))
            fh.close()
            return True
        fh.write("{}\n".format(http_err))
        fh.close()
        return False
    except Exception as err:
        fh.write("{}\n".format(err))
        fh.close()
        return False
    else:
        fh.write('{} test sccess!\n'.format(fullPath))
        return  True

def putApi():
    fh = open("errorLog.txt","a")
    fullPath = 'http://localhost:8010/provider/1'
    try:
        response = requests.put(fullPath, data={'key':'value'})
    except HTTPError as http_err:
        #if api not found
        if response.status_code == 404:
            fh.write("{}\n".format(http_err))
            fh.close()
            return True
        with open("errorLog.txt","a") as fh: 
            fh.write("{}\n".format(http_err))
            fh.close()
        return False
    except Exception as err:
        with open("errorLog.txt","a") as fh: 
            fh.write("{}\n".format(err))
            fh.close()
        return False
    else:
        fh.write('{} test sccess!\n'.format(fullPath))
        return  True

def getProvider():
    global flag2
    for api in ['rates','truck','bill/1?from=t1&to=t2']:
        flag = getApi(portProvider , api)
        if flag == False:
            flag2 = False

def postProvider():
    global flag2
    for api in ['provider','rates', 'truck']:
        flag = postApi(portProvider , api)
        if flag == False:
            flag2 = False

def getWeight():
    global flag2
    for api in ['unknown','weight?from=t1&to=t2&filter=f', 'item/1?from=t1&to=t2', 'session/1']:
        flag = getApi(portWeight , api)
        if flag == False:
            flag2 = False

def postWeight():
    global flag2
    for api in ['batch-weight','weight']:
        flag = postApi(portWeight , api)
        if flag == False: 
            flag2 = False

#main
def testAPI():
    fh = open("errorLog.txt","a")
    fh.write("********** Starting test: ***** time:{} **********\n".format(datetime.now()))
    fh.flush()
    health1 = getApi(portWeight , 'health') 
    health2 = getApi(portProvider , 'health')
    if health1 == False or health2 == False:
        fh.write("Health error \n\n******************** The test is over ********************\n\n")
        re = 'False'
        return re
    else:
        fh.write("Health working\n") 
        fh.flush()     
        getWeight()
        postWeight()
        getProvider()
        postProvider()
        putApi()
    if  flag2 == False:
        fh.write('******************** The test is over api field ********************\n\n')
        fh.close()
        re = 'False'
        return re
    else:
        fh.write('******************** Finished testing test sccess! ********************\n\n')
        fh.close()
        re = 'True'
        return re

if __name__ == "__main__":
    testAPI()