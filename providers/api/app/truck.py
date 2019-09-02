from app import app
from flask import Flask, render_template, redirect, request
from urllib.parse import urlparse
from typing import List, Dict
import mysql.connector
import json
import os
from . import db

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
    cursor.execute('''INSERT INTO Trucks (id,provider_id) VALUES (%s, %s);''', (truckId, providerId))
    connection.commit()
    cursor.execute('select * from Trucks')
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
        return json.dumps(truckPost(trcukId,providerId),sort_keys=True,indent=4)