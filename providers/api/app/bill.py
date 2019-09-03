from app import app
from flask import Flask, redirect, request
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

#    Temporary mock
@app.route('/sesseionMock/<id>', methods=['GET'])
def sessionMOCK(id):
    if request.method == 'GET':
        jsonMock = {
            "bruto": 1200, 
            "containers": "Containers", 
            "datetime": "Mon, 01 Jan 2001 01:01:01 GMT", 
            "direction": "direction", 
            "id": 1235123, 
            "neto": 200, 
            "produce": "produce", 
            "truck": "truck", 
            "truckTara": 1000
            }
    return json.dumps(jsonMock)

@app.route('/bill/<id>',methods=['GET'])
def handleBill(id):
    if request.method == 'GET':
        From=request.args.get('from')
        To=request.args.get('to')
        TruckInfo = json.loads(requests.get('http://localhost:5000/truck/{id}?from=11&to=12').content)
        Bill = {
            "id"   : TruckInfo["id"],
            "name" : "name",
            "from" : From,
            "to"   : To
        }
    return Bill