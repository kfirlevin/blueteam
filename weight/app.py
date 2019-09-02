from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime
import csv
from typing import Dict, List

app = Flask(__name__)

config = {
  'user': 'db',
  'password': 'password',
  'host': 'mysql',
  'port': '3306',
  'database': 'weight',
  'raise_on_warnings': True
}

# execute Query
def exec_query(sql_select_Query):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute(sql_select_Query)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)
        cnx.close()
        return 'Failure', 500
    cnx.close()
    return rows
def executeMany(s1,s2):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.executemany(s1,s2)
        conn.commit()   
    except mysql.connector.Error as err:
        print(err)
        conn.close()
        return 'Failure', 500
    except Error as e:
        print('Error:', e)
    finally:
        cursor.close()
        conn.close()



# @app.route('/weight', methods=['POST'])
# def saveWeight():

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/health', methods=['GET'])
def health():
    # mydb = mysql.connector.connect(**config)
    # print(mydb)
    # return 'mydb'
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(err)
        return 'Failure', 500
    cnx.close()
    return 'OK', 200


@app.route('/weight', methods=['POST'])
def weight_post():
    direction = request.form.get('direction')   
    if direction in ['in', 'out', 'none']:
        return "We're good" , 200        
    else:
        return 'Not a valid direction' , 400




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

@app.route('/unknown', methods=['GET'])
def unknown_weights():

    list_of_unknown = []
    sql_select_Query = "select * from containers_registered"
    rows = exec_query(sql_select_Query)

    for row in rows:
        if  (not row[1]) and (not str(row[1]).isdigit()):
            list_of_unknown.append(row[0])
    return list_of_unknown


@app.route('/batch-weight', methods=['POST'])
def batch_weight():
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
        exec_query(query)
        print(query)
    return ('yo')



#GET /weight?from=t1&to=t2&filter=f
@app.route('/all_con', methods=['GET'])
def get_weight():

    sql_select_Query = """select * from containers_registered"""
    rows = exec_query(sql_select_Query)

    list_of_unknown = []

    for row in rows:
         list_of_unknown.append(
           {
            "container_id": row[0],
            "weight": row[1],
            "unit": row[2]
            }
         )


    return str(list_of_unknown)


## GET /item/<id>?from=t1&to=t2
@app.route('/item', methods=['GET']) # TODO
def get_item():
    sql_select_Query = "select * from containers_registered"
    rows = exec_query(sql_select_Query)

    return str(rows)

# GET /session/<id>
@app.route('/session', methods=['GET']) # TODO
def get_session():
    sql_select_Query = "select * from containers_registered"
    rows = exec_query(sql_select_Query)

    return str(rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)