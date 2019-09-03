from classes import Connection
from flask import  jsonify, abort
import datetime

class Item():

    def get_items(time_from, time_to, id_num):

        time_actual = datetime.datetime.now().strftime("%Y%m%d%I%M%S")


        if id_num is None:
           abort(404)
        if time_from is None:
            t1 = datetime.datetime.now().strftime("%Y%m"+"01000000")
        elif str(time_from).isdigit():
            t1 = time_from
        else:
            abort(404)
        if time_to is None:
            t2 = time_actual
        elif str(time_to).isdigit():
            t2 = time_to
        else:
            abort(404)
        
        list_of_session = []
        tara = None
        
        sql_select_Query = "select * from containers_registered where " + "container_id=" + "'" + str(id_num) + "'"
        rows =  Connection.Mysql.exec_query(sql_select_Query)
        

        if not rows: #if id is not container -> id is truck
            sql_select_Query = "select * from transactions where " + "datetime>='" + str(t1) + "' and datetime<='" + str(t2) + "'" + " and truck=" + "'" + str(id_num) + "'"
            rows =  Connection.Mysql.exec_query(sql_select_Query)
            if not rows:
                abort(404)
            for row in rows:
                if tara is None or row[6] is not None:
                    tara = row[6]
                list_of_session.append(row[0])

            if tara is None:
                tara = "na"
            item = {
                    'id': id_num,
                    'tara': tara,
                    'sessions': list_of_session
            }
            return jsonify({'item': item})

        
        container_weight = rows[0][1]
        sql_select_Query = "select * from transactions where " + "datetime>='" + str(t1) + "' and datetime<='" + str(t2) + "'"
        rows =  Connection.Mysql.exec_query(sql_select_Query)

        for row in rows:
            if id_num in str(row[4]).split(','):
                list_of_session.append(row[0])

        item = {
                'id': id_num,
                'tara': container_weight,
                'sessions': list_of_session
        }
        return jsonify({'item': item})
    
        