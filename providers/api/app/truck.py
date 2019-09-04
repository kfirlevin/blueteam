from app import app
from flask import Flask, render_template, redirect, request
from urllib.parse import urlparse
from typing import List, Dict
import mysql.connector
import json
import requests
import os
from . import db
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

config = {
'user': os.environ.get('DB_USER'),
'password': os.environ.get('DB_PASS'),
'host': os.environ.get('DB_HOST'),
'port': '3306',
'database': 'billdb'
}


def truckPost(truckId,providerId):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "INSERT INTO Trucks (id,provider_id) VALUES (%s, %s);"
    try:
        cursor.execute(query, (truckId, providerId))
        connection.commit()
        logging.info(query,(truckId, providerId))
    except Exception as e:
        logging.error(e)
        return 'error ' + str(e)
    cursor.execute('select * from Trucks')
    results = cursor.fetchall()
    dictionary = {}
    for key, value in results:
        dictionary[key] = value
    cursor.close()
    connection.close()
    return dictionary



def truckPut(truckId,providerId):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "UPDATE Trucks SET provider_id = (select id from Provider where name = %s) where id = %s ;"
    try:
        cursor.execute(query, (providerId, truckId))
        connection.commit()
        logging.info(query, (providerId, truckId))
    except Exception as e:
        logging.error(e)
        return 'error ' + str(e)
    # cursor.execute(query, (providerId, truckId))
    # connection.commit()
    # logging.info(query,(truckId, providerId))
    cursor.execute('select * from Trucks where id = %s ;',(truckId,))
    results = cursor.fetchall()
    dictionary = {}
    for key, value in results:
        dictionary[key] = value 
    cursor.close()
    connection.close()
    return dictionary

def getTrucksByProv(providerid):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'select * from Trucks where provider_id = %s;'%providerid
    logging.info(query)
    try:
        cursor.execute(query)
        logging.info(str(query))
    except Exception as e:
        logging.error(e)
        return 'error ' + str(e)
    results = cursor.fetchall()
    dictionary = {}
    for key, value in results:
        dictionary[key] = value
    cursor.close()
    connection.close()
    return dictionary


#  Routing -->
@app.route('/truck',methods=['POST','PUT'])
def handleTruck():
    if request.method == 'POST':
        trcukId=request.args.get('id')
        providerId=request.args.get('provider')
        res = truckPost(trcukId,providerId)
        if 'error' in str(res):
            return str(res),500
        return json.dumps(res,sort_keys=True,indent=4)
    
    if request.method == 'PUT':
        trcukId=request.args.get('id')
        providerId=request.args.get('provider')
        res = truckPut(trcukId,providerId)
        if 'error' in str(res):
            return str(res),500
        return json.dumps(res,sort_keys=True,indent=4)

#specific truck
@app.route('/truck/<id>',methods=['GET'])
def handleTruckGet(id):
    if request.method == 'GET':
        From=request.args.get('from')
        To=request.args.get('to')
        jsonMOCK = {
            "id" : 123,
            "tara" : 2000,
            "sessions" : [1]
        }
        return jsonMOCK

# get all trucks of specific provider
@app.route('/trucksbyprov/<providerid>',methods=['GET'])
def handleProviderId(providerid):
    return getTrucksByProv(providerid)


# @app.route('/truck/<id>',methods=['GET'])
# def handleTruckGet(id):
#     if request.method == 'GET':
#         From=request.args.get('from')
#         To=request.args.get('to')
#         weightjson = requests.get('http://blue.develeap.com:8090/item/{id}?from={From}&to={To}')
#         return requests.get('http://localhost:5000/test').content
        

