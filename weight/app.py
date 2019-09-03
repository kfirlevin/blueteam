from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime
from typing import Dict, List
from classes import Connection
from classes.Weight import Weight
from classes.Item import Item
from classes.Transaction import Transaction
import os

app = Flask(__name__)
config = {
  'user': 'db',
  'password': 'password',
  'host': os.environ.get('MYSQL_HOST'),
  'port': '3306',
  'database': 'weight',
  'raise_on_warnings': True
}


# @app.route('/weight', methods=['POST'])
# def saveWeight():


# Author:
# TODO Add Comments - Description
@app.route('/')
def index():
    return render_template("index.html")


# Author:
# TODO Add Comments - Description
@app.route('/health', methods=['GET'])
def health():
    return Connection.Mysql.health()

# Author:
# TODO Add Comments - Description
@app.route('/weight', methods=['POST'])
def weight_post():
    if request.method == 'GET':
            return render_template("weight-form.html")
    elif request.method == 'POST':
        id = request.form.get('id')
        datetime = request.form.get('datetime')
        direction = request.form.get('direction')
        truck = request.form.get('truck')
        containers = request.form.get('containers')
        bruto = request.form.get('bruto')
        truckTara = request.form.get('truckTara')
        produce = request.form.get('produce')
    if Connection.Mysql.isHealth() == True : 
        return Weight.weight_post(direction)
    return "Error: DB Connection"

    
# Author:
# TODO Add Comments - Description
@app.route('/weight', methods=['GET'])
def weights_get():
    if Connection.Mysql.isHealth() == True : 
        return Weight.weights_get(request.args.get('from'),request.args.get('to'),request.args.get('filter'))
    return "Error: DB Connection"


    
# Author:
# TODO Add Comments - Description
@app.route('/unknown', methods=['GET'])
def unknown_weights():
    if Connection.Mysql.isHealth() == True : 
        return Weight.unknown_weights()
    return "Error: DB Connection"


# Author:
# TODO Add Comments - Description
@app.route('/batch-weight',  methods = ['GET', 'POST'])
def batch_weight():
    if request.method == 'GET':
        return render_template("betch-weight.html")
    elif request.method == 'POST':
        if Connection.Mysql.isHealth() == True : 

            fileName = request.form.get('file')        
            return Weight.batch_weight(fileName)

        return "Error: DB Connection"
        



# Author:
# TODO Add Comments - Description
#GET /weight?from=t1&to=t2&filter=f
@app.route('/all_con', methods=['GET'])
def get_weight():

    sql_select_Query = """select * from containers_registered"""
    rows = Connection.Mysql.exec_query(sql_select_Query)

    list_of_unknown = []

    for row in rows:
         list_of_unknown.append(
           {
            "container_id": row[0],
            "weight": row[1],
            "unit": row[2]
            }
         )
    return jsonify(list_of_unknown)


# Author:
# TODO Add Comments - Description
#GET /weight?from=t1&to=t2&filter=f
@app.route('/all_transactions', methods=['GET'])
def get_transaction():

    sql_select_Query = """select * from transactions"""
    rows = Connection.Mysql.exec_query(sql_select_Query)

    list_of_unknown = []

    for row in rows:
         list_of_unknown.append(
             Transaction.transactionToJson(row)
         )
    return jsonify(list_of_unknown)

# Author:
# TODO Add Comments - Description
## GET /item/<id>?from=t1&to=t2
@app.route('/item/<string:id_num>', methods=['GET']) # TODO
def get_item(id_num):
    if Connection.Mysql.isHealth() == True : 
        return Item.get_items(request.args.get('from'),request.args.get('to'),id_num)
    return "Error: DB Connection"


# Author: 
# TODO Add Comments - Description
#   GET /session/<id>
@app.route('/session/<string:id_num>', methods=['GET']) # TODO
def get_session(id_num):
    if Connection.Mysql.isHealth() == True : 
        return Transaction.get_session(id_num)
    return "Error: DB Connection"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
