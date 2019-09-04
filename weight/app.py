from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime
from typing import Dict, List
from classes import Connection
from classes.Weight import Weight
from classes.Item import Item
from classes.Transaction import Transaction
import os
import logging

app = Flask(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
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
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.warning('is when this event was logged.')
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
            return 'Not a valid direction', 404
        truckId = request.form.get('truck')
        if truckId is None:
            return 'No truck id?', 404
        time_actual = datetime.datetime.now().strftime("%Y%m%d%I%M%S")
        containers = request.form.get('containers')
        if containers is None:
            return 'There are no containers?', 404
        bruto = request.form.get('bruto')
        if bruto is None:
            return 'You forgot to enter weight', 404
        produce = request.form.get('produce')
        if produce not in ("tomato", "orange"):
            return 'Not a valid produce', 404
        if request.form.get('force') == 'true':
            force = True


        if truckId == "na":
            query="INSERT INTO transactions(datetime,direction,truck,containers,bruto,produce) VALUES(" + time_actual + "," + "'" +direction+ "'"+","+"'"+truckId+"'" +","+ "'"+containers+"'"+","+bruto+","+ "'"+produce+ "'"+")"
            Connection.Mysql.exec_query(query)
            return "na to do"
        

        data=Weight.last_action(truckId,True)
        if direction == "in":
            if data == "not found" or data[2] == 'out':
                query="INSERT INTO transactions(datetime,direction,truck,containers,bruto,produce) VALUES(" + time_actual + "," + "'" +direction+ "'"+","+"'"+truckId+"'" +","+ "'"+containers+"'"+","+bruto+","+ "'"+produce+ "'"+")"
                Connection.Mysql.exec_query(query)
            elif data[2] == 'in':
                if force:
                    pass
                else:
                    pass
        elif direction == "out":
            if data == "not found":
                abort(404)
            elif data[2] == 'in':
                if not Weight.all_containers_here(str(containers).split(',')):
                    return "containers not known in out", 404
                else:
                    if any(x in str(row[4]).split(',') for x in Weight.unknown_weights()):
                        neto = "na"
                    else:
                        sum_weight_containers = 0
                        for id_num in str(containers).split(','):
                            sum_weight_containers = sum_weight_containers + Weight.container_weight(id_num)
                        neto = data[5] - sum_weight_containers - bruto
                    
                    query="INSERT INTO transactions(datetime,direction,truck,containers,bruto,truckTara,neto,produce) VALUES(" + time_actual + "," + "'" +direction+ "'"+","+"'"+truckId+"'" +","+ "'"+containers+"'"+","+bruto+","+ "'"+produce+ "'"+")"
                    session = {
                    'id': truckId, # id of new transaction
                    'truck': truckId,
                    'bruto': data[5], #bruto of in
                    'truckTara': bruto,
                    'neto': neto
                    }




            elif data[2] == 'out':
                if force:
                    pass #copy from nave
                else:
                    abort(404)
        else: #direction=out
            if data[2] == 'in':
                abort(404)
            else:
                query="INSERT INTO transactions(datetime,direction,truck,containers,bruto,produce) VALUES(" + time_actual + "," + "'" +direction+ "'"+","+"'"+truckId+"'" +","+ "'"+containers+"'"+","+bruto+","+ "'"+produce+ "'"+")"
                Connection.Mysql.exec_query(query)

        return("good"), 200

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
        return Weight.last_action(id_num,True)
    return "Error: DB Connection"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
