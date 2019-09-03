from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime
import csv
import json
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
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(err)
        return 'Failure', 500

    time_actual = datetime.datetime.now().strftime("%Y%m%d%I%M%S")

    if request.args.get('from')is None:
        t1 = datetime.datetime.now().strftime("%Y%m%d"+"000000")
    else:
        t1 = request.args.get('from')
    
    if request.args.get('to')is None:
        t2 = time_actual
    else:
        t2 = request.args.get('to')
    f = []
    if request.args.get('filter')is None:
        f = ["in","out","none"]
    else:
        f = str(request.args.get('filter')).split(',')
    
    sql_select_Query = "select * from transactions where " + "datetime>='" + str(t1) + "' and datetime<='" + str(t2) + "'"
    cursor = cnx.cursor()
    cursor.execute(sql_select_Query)
    rows = cursor.fetchall()

    list_of_transactions = []

    for row in rows:
        if row[2] in f:
            if any(x in str(row[4]).split(',')  for x in unknown_weights()): #na if some of containers have unknown tara
                neto = None
            else:
                neto = row[7]
            transact = {
                'id': row[0],
                'direction': row[2],
                'bruto': row[5],
                'neto': neto,
                'produce': row[8],
                'containers': str(row[4]).split(',') 
            }
            list_of_transactions.append(transact)
        
    return jsonify({'transactions': list_of_transactions})

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
        ids=[]
        weights=[]
        convert=False
        fileName = request.form.get('file')
        print(type(fileName))
        print(fileName)
        if fileName.endswith('.csv'):
            try:
                spamReader = csv.reader(open('./in/'+fileName, newline=''), delimiter=',', quotechar='|')
                ids=[]
                weights=[]
                for row in spamReader:
                    ids.append(row[0])
                    weights.append(row[1])
                if str(weights[0]) == '"lbs"':
                    convert=True
                weights.pop(0)
                ids.pop(0)
            except IOError as e: # TODO write to LOGFILE
                print ('I/O error({0}): {1}'.format(e.errno, e.strerror))
                return ('I/O error({0}): {1}'.format(e.errno, e.strerror))

        elif fileName.endswith('.json'):
            try:
                with open('./in/'+fileName) as json_file:
                    data=json.loads(json_file.read())
                if data[1]["unit"]=='lbs':
                    convert = True
                for truck in data:
                    ids.append(truck["id"])
                    weights.append(truck["weight"])
            except IOError as e: # TODO write to LOGFILE
                print ('I/O error({0}): {1}'.format(e.errno, e.strerror))
                return ('I/O error({0}): {1}'.format(e.errno, e.strerror))
              
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
@app.route('/item', methods=['GET']) # TODO
def get_item():
    sql_select_Query = "INSERT INTO `transactions` (`id`, `datetime`, `direction`, `truck`, `containers`, `bruto`, `truckTara`, `neto`, `produce`) VALUE ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (1235123, 20010101010101 , "direction" , "truck" , "Containers" , 1200 , 1000 , 200 , "produce");
    rows = Connection.Mysql.exec_query(sql_select_Query)
    return str(rows)

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
