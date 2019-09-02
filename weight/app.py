from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

config = {
  'user': 'db',
  'password': 'password',
  'host': 'mysql',
  'port': '3306',
  'database': 'weight_db',
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
    if direction != 'in' or direction != 'out' or direction != 'none':
        return 'Not a valid direction' , 400
    else:
        return "We're good" , 200

# @app.route('/')
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)