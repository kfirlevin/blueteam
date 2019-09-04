from app import app
from flask import Flask, redirect, request
from urllib.parse import urlparse
from typing import List, Dict
import mysql.connector
import json
import pandas as ps
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
@app.route('/sessionMock/<id>', methods=['GET'])
def sessionMOCK(id):
    jsonMock = {
        "bruto": 1200, 
        "containers": "Containers", 
        "datetime": "Mon, 01 Jan 2001 01:01:01 GMT", 
        "direction": "direction", 
        "id": 1235123, 
        "neto": 200, 
        "produce": "blood", 
        "truck": "truck", 
        "truckTara": 1000
        }
    return jsonMock

@app.route('/bill/<id>',methods=['GET'])
def handleBill(id):
        From=request.args.get('from')
        To=request.args.get('to')
        trucksIdsByProv = json.loads(requests.get(f'http://localhost:5000/trucksbyprov/{id}').content)
        allTrucksInfo = []
        allSessions = []
        total_payment = 0
        ratesfile = ps.read_excel(f'http://localhost:5000/rates')
        #ratesfile = ps.read_excel("rates.xlsx",sheet_name = "rates")
        # getting relevant rates by provider 
        ref_dict = {}
        for index, row in ratesfile.iterrows():
            if str(id) == str(row["Scope"]) or row["Scope"] == "All":
                ref_dict[str(row["Product"]).lower()] = row["Rate"]

        sessionCount = 0
        for truckID in trucksIdsByProv:
            allTrucksInfo.append(json.loads(requests.get(f'http://localhost:5000/truck/{truckID}?from=11&to=12').content))

        for truckData in allTrucksInfo:
            sessionCount += len(truckData["sessions"])
            for sessionid in truckData["sessions"]:
                allSessions.append(json.loads(requests.get(f'http://localhost:5000/sessionMock/{sessionid}').content))

        Bill = {
            "id"   : id,
            "name" : "name",
            "from" : From,
            "to"   : To,
            "truckCount":len(allTrucksInfo),
            "sessionCount": sessionCount,
            "products":[] , 
            "total" : 0
        }
        Bill["products"].append({
            "product" : "tomato" ,
            "count" : 1 ,
            "amount": 500 ,
            "rate"  : 0 ,
            "pay"   : 1000
        })
        logging.info(Bill["products"])
        for sessionData in allSessions:
            new_product = str(sessionData["produce"]).lower()
            logging.info(sessionData["produce"])
            for index in Bill["products"]:
                existing_product = str(index["product"]).lower()
                if existing_product == new_product:
                    index.update({
                        "product": sessionData["produce"] ,
                        "count" : index["count"]+1 ,
                        "amount": index["amount"]+sessionData["neto"] ,
                        "rate"  : ref_dict[new_product] ,
                        "pay"   : index["pay"]+(sessionData["neto"]*ref_dict[new_product])
                    })
                else:
                    Bill["products"].append({
                        "product" : sessionData["produce"] ,
                        "count" : 1 ,
                        "amount": sessionData["neto"] ,                      
                        "rate"  : ref_dict[new_product] ,
                        "pay"   : sessionData["neto"]*ref_dict[new_product]
                    })
                total_payment += index["pay"]
        Bill["total"] = total_payment
        logging.info(Bill)
        return "A"