from classes import Connection
from flask import  jsonify

class Weight():


    def weight_post(direction):
        if direction in ['in', 'out', 'none']:
            return "We're good" , 200        
        else:
            return 'Not a valid direction' , 400
    
    def unknown_weights():
        list_of_unknown = []
        sql_select_Query = "select * from containers_registered"
        rows = Connection.Mysql.exec_query(sql_select_Query)

        for row in rows:
            if  (not row[1]) and (not str(row[1]).isdigit()):
                list_of_unknown.append(row[0])
        return jsonify({'list_of_unknown': list_of_unknown})