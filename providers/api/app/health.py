from app import app
from flask import Flask, render_template, redirect, request, Response
from urllib.parse import urlparse
from typing import List, Dict
import mysql.connector
import json
import os
import logging
import sys 

logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)
from . import db

def health():
    config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
    'host': os.environ.get('DB_HOST'),
    'port': '3306',
    'database': 'billdb'
    }
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('SELECT 1;')
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return 0
    except:
        return 1

@app.route('/health')
def handle_health():
    res = health()
    if res == 0:
        logging.info('HEALTH!')
        return """<html><body><pre>
 ___ _,_ _  _,       _  _,        _,       _,_ __,  _, _,  ___ _,_ , _  
  |  |_| | (_        | (_        /_\       |_| |_  /_\ |    |  |_| \ |  
  |  | | | , )       | , )       | |       | | |   | | | ,  |  | |  \|  
  ~  ~ ~ ~  ~        ~  ~        ~ ~       ~ ~ ~~~ ~ ~ ~~~  ~  ~ ~   )  
                                                                    ~'  
     __, __,  _, __,  _, _, _  _, __,                                   
     |_) |_  (_  |_) / \ |\ | (_  |_                                    
     | \ |   , ) |   \ / | \| , ) |                                     
     ~ ~ ~~~  ~  ~    ~  ~  ~  ~  ~~~                                   </pre></body></html>
"""
    else:
        logging.error('HEALTH ERROR!')
        return Response('server error', status=500)