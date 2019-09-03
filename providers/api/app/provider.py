from app import app
from flask import Flask, render_template, redirect, request, make_response
from urllib.parse import urlparse
from typing import List, Dict
import mysql.connector
import os
import logging
import sys 

logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)

def sql(value):
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
        cursor.execute(f"INSERT INTO Provider (`name`) VALUES ('{value}')")
        cursor.execute(f"SELECT id from Provider WHERE name='{value}' ")
        re=cursor.fetchall()
        cursor.close()
        connection.close()
        logging.info(f"INSERT {value} INTO PROVIDER")
        return re
    except Exception as e:
        logging.error(e)
        return 'error ' + str(e)

@app.route('/provider', methods=["POST"])
def provider():
    value=request.args["provider_name"]
    res=sql(value)
    if 'error' in str(res):
            return res
    v1=res[0]
    return "{\"id\":\""+str(v1[-1])+"\"}"