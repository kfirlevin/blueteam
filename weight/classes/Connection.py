import mysql.connector
import os
import logging

config = {
    'user': 'db',
    'password': 'password',
    'host': os.environ.get('DB_HOST'),
    'port': '3306',
    'database': 'weight',
    'raise_on_warnings': True
}


class Mysql(object):

    @staticmethod      # execute Query
    def exec_query(sql_select_Query):
        try:
            logging.warning("execute Query :  {} ".format(str(sql_select_Query)))
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute(sql_select_Query)
            rows = cursor.fetchall()
            cnx.close()
            return rows
        except mysql.connector.Error as err:
            logging.warning("Error execute Query :  {} ".format(str(err)))
            return 'Failure', 500, err
        

    @staticmethod
    def health():
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print(err)
            return 'Failure', 500
        cnx.close()
        return 'OK', 200

    @staticmethod
    def isHealth():
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print(err)
            return False
        cnx.close()
        return True
