from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode
import csv

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
    return rows;



# @app.route('/weight', methods=['POST'])
# def saveWeight():

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

@app.route('/unknown', methods=['GET'])
def unknown_weights():

    list_of_unknown = []
    sql_select_Query = "select * from containers_registered"
    rows = exec_query(sql_select_Query)
  
@app.route('/batch-weight', methods=['POST'])
def batch_weight():
    fileName = request.form.get('file')
    # file=open("in/"+fileName,'r')
    # data=file.read()
    # file.close()
    spamReader = csv.reader(open('./in/'+fileName, newline=''), delimiter=',', quotechar='|')
    #print(spamReader.headline)
    ids=[]
    weights=[]
    for row in spamReader:
        ids.append(row[0])
        weights.append(row[1])
        # print(row[1])
        # print(type(row))
        print(row)
        #print(', '.join(row))
    if str(weights[0]) == '"lbs"':
        convert=True
    else:
        convert=False
    weights.pop(0)
    ids.pop(0)
    if convert:
        for i in range (len(weights)):
            #item=(0.453592*float(item))
            weights[i] = str(int(0.453592*float(weights[i])))
    for i in range(len(ids)):
        print("id:"+ids[i]+", weight: "+weights[i])
#@app.route('/batch_weight', methods=['POST'])
#    for row in rows:
 #       if  not str(row[1]).isdigit():
  #          list_of_unknown.append(row[0])
   # return str(list_of_unknown)
    return ("ok?")



#GET /weight?from=t1&to=t2&filter=f
@app.route('/weight', methods=['GET'])
def get_weight():

    sql_select_Query = """select * from containers_registered"""
    rows = exec_query(sql_select_Query)

    return str(rows)


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