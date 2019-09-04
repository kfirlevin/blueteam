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
  'host': os.environ.get('DB_HOST'),
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
        force = False
        direction = request.form.get('direction')
        if direction not in ("out", "in", "none"):
            return 'Not a valid direction', 400
        if direction == 'none':
            direction = 'in'
        truck = request.form.get('truck')
        if truck is None:
            return 'No truck id?', 400
        datetime = datetime.datetime.now()
        containers = request.form.get('containers').split(',')
        if containers is None:
            return 'There are no containers?', 400
        weight = request.form.get('weight')
        if weight is None:
            return 'You forgot to enter weight', 400
        unit = request.form.get('unit')
        if unit not in ("kg", "lbs"):
            return 'unit not supported', 400
        if unit == 'lbs':
            weight = int(0.453592*float(weight))
            unit = 'kg'
        produce = request.form.get('produce')
        if produce not in ("tomato", "orange"):
            return 'Not a valid produce', 400
        if request.form.get('fouce') == 'true':
            force = True

    if Connection.Mysql.isHealth() == True:
        return Weight.weight_post(direction)
    return "Error: DB Connection"

    
# Author:
# TODO Add Comments - Description
@app.route('/weight', methods=['GET'])
def weights_get():
    if Connection.Mysql.isHealth() == True:
        return Weight.weights_get(request.args.get('from'), request.args.get('to'), request.args.get('filter'))
    return "Error: DB Connection"


# Author:
# TODO Add Comments - Description
@app.route('/unknown', methods=['GET'])
def unknown_weights():
    if Connection.Mysql.isHealth() == True:
        return Weight.unknown_weights()
    return "Error: DB Connection"


# Author:
# TODO Add Comments - Description
@app.route('/batch-weight',  methods=['GET', 'POST'])
def batch_weight():
    if request.method == 'GET':
        return render_template("betch-weight.html")
    elif request.method == 'POST':
        if Connection.Mysql.isHealth() == True:

            fileName = request.form.get('file')        
            return Weight.batch_weight(fileName)

        return "Error: DB Connection"
        

# Author:
# TODO Add Comments - Description
# GET /weight?from=t1&to=t2&filter=f
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
# GET /weight?from=t1&to=t2&filter=f
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
# GET /item/<id>?from=t1&to=t2
@app.route('/item/<string:id_num>', methods=['GET'])  # TODO
def get_item(id_num):
    if Connection.Mysql.isHealth() == True:
        return Item.get_items(request.args.get('from'), request.args.get('to'), id_num)
    return "Error: DB Connection"


# Author: 
# TODO Add Comments - Description
#   GET /session/<id>
@app.route('/session/<string:id_num>', methods=['GET'])  # TODO
def get_session(id_num):
    if Connection.Mysql.isHealth() == True:
        return Transaction.get_session(id_num)
    return "Error: DB Connection"

@app.route('/container_weight/<string:id_num>', methods=['GET'])  # TODO
def container_weight(id_num):
    if Connection.Mysql.isHealth() == True:
        return Weight.container_weight(id_num)
    return "Error: DB Connection"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
