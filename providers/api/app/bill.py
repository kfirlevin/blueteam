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

def buildPath(host,route,id=""):
    return host + "/" + route + "/" + id

def buildUrlParams(urlstr,params):
    urlstr += "?"
    for key in params:
        urlstr += str(key) + "=" + str(params[key]) 



#    Temporary mock
@app.route('/sessionMock/<id>', methods=['GET'])
def sessionMOCK(id):
    From=request.args.get('from')
    To=request.args.get('to')
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
        sessionCount = 0
        hostlocal = os.environ.get('DB_HOST')
        hostprod = "http://blue.develeap.com:8090"
        ratesfile = ps.read_excel(f'http://localhost:5000/rates')
        weighthost = os.environ.get('WEIGHT_HOST')

        # getting relevant rates by provider 
        ref_dict = {}
        for index, row in ratesfile.iterrows():
            if str(id) == str(row["Scope"]) or row["Scope"] == "All":
                ref_dict[str(row["Product"]).lower()] = row["Rate"]

        #session_request_path = buildPath(hostprod, "session", id=id)
        if From:
            if To:
                urlparams = f'?from={From}&to={To}'
            else:
                urlparams = f'?from={From}'
        else:
            if To:
                urlparams = f'?to={To}'
            else:
                urlparams = f''
        for truckID in trucksIdsByProv:
            try:
                path=buildPath('http://localhost:5000', "truck", id=str(truckID))
                logging.info('path: '+path)
                req = requests.get(path + urlparams)
                logging.info('req: '+req)
                allTrucksInfo.append(json.loads(req.content)["item"])
            except Exception:
                pass
        logging.info(allTrucksInfo)
        logging.info("LOGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
        for truckData in allTrucksInfo:
            sessionCount += len(truckData["sessions"])
            logging.info('sessionCount: ' + str(sessionCount))
            for sessionid in truckData["sessions"]:
                logging.info('sessionid: '+ str(sessionid))
                try:
                    logging.info(buildPath(hostlocal, "session", id=str(sessionid)))
                    tmp = json.loads(requests.get(buildPath(hostlocal, "session", id=str(sessionid)) + urlparams).content)
                    
                    logging.info(tmp)
                    logging.info('tmp')
                    if tmp["direction"] == "out":
                        allSessions.append(tmp)
                        #allSessions.append(json.loads(requests.get(f'http://blue.develeap.com:8090/session/{sessionid}').content))
                except Exception:
                    pass
        try:
            name = json.loads(requests.get(f'http://localhost:5000/provider/{id}').content)["name"]
        except Exception:
            name = "not exist"
        Bill = {
            
            "id"   : id,
            "name" : name ,
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
        for sessionData in allSessions:
            new_product = str(sessionData["produce"]).lower()
            for index in Bill["products"]:
                existing_product = str(index["product"]).lower()
                flag_update = 0
                if existing_product == new_product:
                    flag_update = 1
                    index.update({
                        "product": sessionData["produce"] ,
                        "count" : index["count"]+1 ,
                        "amount": index["amount"]+sessionData["neto"] ,
                        "rate"  : ref_dict[new_product] ,
                        "pay"   : index["pay"]+(sessionData["neto"]*ref_dict[new_product])
                    })
                    total_payment += index["pay"]
            # if product does not exist, creat one    
            if flag_update == 0:
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
        return Bill