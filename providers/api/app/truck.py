from app import app
from flask import Flask, render_template, redirect, request
from urllib.parse import urlparse
from typing import List, Dict
import mysql.connector
import json
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
    cursor.execute(query, (truckId, providerId))
    connection.commit()
    logging.info(query,(truckId, providerId))
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
    cursor.execute(query, (providerId, truckId))
    connection.commit()
    cursor.execute('select * from Trucks where id = %s ;',(truckId,))
    results = cursor.fetchall()
    dictionary = {}
    for key, value in results:
        dictionary[key] = value 
    cursor.close()
    connection.close()
    return dictionary

@app.route('/truck',methods=['GET','POST','PUT'])
def handleTruck():
    if request.method == 'POST':
        trcukId=request.args.get('id')
        providerId=request.args.get('provider')
        #res = truckPost(trcukId,providerId)
        return json.dumps(truckPost(trcukId,providerId),sort_keys=True,indent=4)
    
    if request.method == 'PUT':
        trcukId=request.args.get('id')
        providerId=request.args.get('provider')
        return json.dumps(truckPut(trcukId,providerId),sort_keys=True,indent=4)