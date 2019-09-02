from app import app
from flask import request, send_from_directory
import pandas as ps
from pandas import ExcelFile
import mysql.connector
import os
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

last_file_name = ''


@app.route('/rates', methods=['GET', 'POST'])
def rates():
    if request.method == 'POST':
        config = {
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASS'),
            'host': os.environ.get('DB_HOST'),
            'port': '3306',
            'database': 'billdb'
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        file = request.args.get('file')
        global last_file_name
        last_file_name = file
        df = ps.read_excel('/in/' + file, sheet_name='rates')
        try:
            cursor.execute('DELETE FROM Rates')
        except:
            return '', 500
        sql = 'INSERT INTO Rates (product_id, rate, scope) values '
        lines = []
        for i in df.index:
            lines.append('("' + str(df['Product'][i]) + '", ' +
                         str(df['Rate'][i]) + ', "' + str(df['Scope'][i]) +
                         '")')
        sql += ', \n'.join(lines)
        logging.info(sql)
        try:
            cursor.execute(sql)
        except:
            return '', 500
        return ''
    elif request.method == 'GET':
        return send_from_directory(directory='/in/',
                                   filename=last_file_name,
                                   as_attachment=True)
    cursor.close()
    connection.close()
    return "rates"