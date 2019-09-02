from app import app
from flask import Flask, render_template, redirect, request, make_response
from urllib.parse import urlparse
from typing import List, Dict
import mysql.connector
import json
import os
from . import db

def health():
    config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
    'host': os.environ.get('DB_HOST'),
    'port': '3306',
    'database': 'billdb'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT 1;')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.route('/health')
def handle_health():
    res = health()
    if res:
        resp = make_response()
        resp.headers['Content-Type'] = 'text/plain'
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