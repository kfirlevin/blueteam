from app import app
from flask import request
import pandas as ps
from pandas import ExcelFile
import mysql.connector
import os
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@app.route('/rates', methods=['GET', 'POST'])
def rates():
    config = {
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASS'),
        'host': os.environ.get('DB_HOST'),
        'port': '3306',
        'database': 'billdb'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    if request.method == 'POST':
        file = request.args.get('file')
        df = ps.read_excel('/in/' + file, sheet_name='rates')
        cursor.execute('DELETE FROM Rates')
        sql = 'INSERT INTO Rates (product_id, rate, scope) values '
        lines = []
        for i in df.index:
            lines.append('("' + str(df['Product'][i]) + '", ' +
                         str(df['Rate'][i]) + ', "' + str(df['Scope'][i]) +
                         '")')
        sql += ', \n'.join(lines)
        logging.info(sql)
        cursor.execute(sql)
    elif request.method == 'GET':
        sql = 'SELECT * from Rates'
        cursor.execute(sql)
        logging.info(sql)
        results = ''
        try:
            results = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            results = e
        return results
    cursor.close()
    connection.close()
    return "rates"