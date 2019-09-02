import mysql.connector


config = {
    'user': 'db',
    'password': 'password',
    'host': 'weight-db',
    'port': '3306',
    'database': 'weight',
    'raise_on_warnings': True
}


class Mysql(object):

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
    
    def health():
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print(err)
            return 'Failure', 500
        cnx.close()
        return 'OK', 200

    def isHealth():
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print(err)
            return False
        cnx.close()
        return True
    



        