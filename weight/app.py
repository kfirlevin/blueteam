from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime
import csv

from typing import Dict, List

from classes import Connection
from classes.Weight import Weight
from classes.Transaction import Transaction


app = Flask(__name__)

config = {
  'user': 'db',
  'password': 'password',
  'host': 'weight-db',
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
    direction = request.form.get('direction')
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
        try:
            fileName = request.form.get('file')
            spamReader = csv.reader(open('./in/'+fileName, newline=''), delimiter=',', quotechar='|')
            ids=[]
            weights=[]
            for row in spamReader:
                ids.append(row[0])
                weights.append(row[1])
                #print(row)
            if str(weights[0]) == '"lbs"':
                convert=True
            else:
                convert=False
            weights.pop(0)
            ids.pop(0)
            if convert:
                for i in range (len(weights)):
                    weights[i] = str(int(0.453592*float(weights[i])))
                    ids[i]='"' + ids[i] + '"'
            for i in range(len(ids)):
                #print("id:"+ids[i]+", weight: "+weights[i])
                #toSend.append("('{}', '{}', 'kg')".format(ids[i], weights[i]))
                query = "INSERT INTO containers_registered(container_id,weight,unit) VALUES(%s,%s,'kg');" % (ids[i],weights[i])
                print(query)
                Connection.Mysql.exec_query(query)
                print(query)
                return "OK"

        except IOError as e: # TODO write to LOGFILE
              print ('I/O error({0}): {1}'.format(e.errno, e.strerror))
              return ('I/O error({0}): {1}'.format(e.errno, e.strerror))

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
        return Weight.get_items(request.args.get('from'),request.args.get('to'),id_num)
    return "Error: DB Connection"
    

# Author:
# TODO Add Comments - Description
#   GET /session/<id>
@app.route('/session', methods=['GET']) # TODO
def get_session():
    sql_select_Query = "select * from containers_registered"
    rows = Connection.Mysql.exec_query(sql_select_Query)
    return str(rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
