from app import app
from flask import Flask, render_template, redirect, request, make_response
from urllib.parse import urlparse
from typing import List, Dict
import mysql.connector
import os
import logging
import sys 

logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)

def sql(value,req):
    config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
    'host': os.environ.get('DB_HOST'),
    'port': '3306',
    'database': 'billdb'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    try:
        cursor.execute(value)
        if(req):
                re=cursor.fetchall()
                if(re==[]):
                        re="ERROR"
        else:
                re="OK"
        cursor.close()
        connection.close()
        return re
    except:
        logging.error(f"{value} FAILED!!!!!")
        return "ERROR"


@app.route('/provider', methods=["GET"])
def provider_get():
        return "WELCOME to providers please use PUT or POST request"

@app.route('/provider', methods=["POST"])
def provider():
        value=request.args["provider_name"]
        logging.info(f"INSERT {value} INTO PROVIDER")
        sql(f"INSERT INTO Provider (`name`) VALUES ('{value}')",False)
        hh=sql(f"SELECT id from Provider WHERE name='{value}' ",True)
        if (hh != "ERROR"):
                v1=hh[0]
                return "{\"id\":\""+str(v1[-1])+"\"}"     

@app.route('/provider/<id>', methods=["PUT"])
def provider_put(id):
        provider_name=request.args["provider_name"]
        hh1=sql(f"SELECT id FROM Provider WHERE id = {id}",True)
        if(hh1 !="ERROR"):
                hh=sql(f"UPDATE Provider SET name = '{provider_name}' WHERE id = {id}",False)
                logging.info(f"UPDATE {id} TO {provider_name}")
                if (hh != "ERROR" ):
                        return "VALUE UPDATED" 
        else:
                logging.error(f"{id} NOT FOUND")
                return (f"{id} NOT FOUND",404)




