from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

config = {
  'user': 'db',
  'password': 'password',
  'host': 'localhost',
  'port': '777',
  'database': 'mydb',
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
    


if __name__ == '__main__':
    app.run()