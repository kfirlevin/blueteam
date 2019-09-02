from app import app
from flask import Flask, render_template, redirect, request, make_response
from urllib.parse import urlparse
from typing import List, Dict
import mysql.connector
import json
import os
import logging
import sys 

logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)

def sql(value):
    config = {
    'user': "root",
    'password': "root",
    'host': "localhost",
    'port': '5010',
    'database': 'billdb'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    try:
        cursor.execute(f"INSERT INTO Provider (`name`) VALUES ('{value}')")
        cursor.execute(f"SELECT id from Provider WHERE name='{value}' ")
        re=cursor.fetchall()
        cursor.close()
        connection.close()
        return re
    except:
        return "ERROR"

@app.route('/provider', methods=["POST"])
def provider():
    value=request.args["provider_name"]
    logging.info(f"INSERT {value} IN TO PROVIDER")
    hh=sql(value)
    if (hh != "ERROR"):
        v1=hh[0]
        return "{\"id\":\""+str(v1[-1])+"\"}"