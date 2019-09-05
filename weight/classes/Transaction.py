from classes import Connection
from flask import jsonify, abort
import datetime


class Transaction():
    
    @staticmethod
    def transactionToJson(row):
        return {
            "id": row[0],
            "datetime": row[1],
            "direction": row[2],
            "truck": row[3],
            "containers": row[4],
            "bruto": row[5],
            "truckTara": row[6],
            "neto": row[7],
            "produce": row[8]
        }
    @staticmethod
    def get_session(id_num):

        time_actual = datetime.datetime.now().strftime("%Y%m%d%I%M%S")

        if not str(id_num).isdigit():
            abort(404)

        list_of_session = []

        sql_select_Query = "select * from transactions where " + \
            "id=" + "'" + str(id_num) + "'"
        rows = Connection.Mysql.exec_query(sql_select_Query)

        if not rows:  # if id is not container -> id is truck
            abort(404)

        if rows[0][7] is None:
            neto = "na"
        else:
            neto = rows[0][7]

        if rows[0][2] == "out":
            session = {
                'id': id_num,
                'direction': rows[0][2],
                'truck': rows[0][3],
                'bruto': rows[0][5],
                'truckTara': rows[0][6],
                'neto': neto,
                'produce': rows[0][8]
            }
        else:
            session = {
                'id': id_num,
                'direction': rows[0][2],
                'truck': rows[0][3],
                'bruto': rows[0][5],
                'produce': rows[0][8]

            }
        return jsonify({'session': session})
