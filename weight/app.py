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

    return ("ok?")
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)