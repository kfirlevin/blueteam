from classes import Connection
from flask import jsonify, abort
import datetime
from classes.Weight import Weight

import logging
class Item():

    @staticmethod
    def get_items(time_from, time_to, id_num):
        
        # init Logging
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        # get current time 
        time_actual = datetime.datetime.now().strftime("%Y%m%d%I%M%S")
        

        ##############################    Valid item_id argument      ###########################
        if id_num is None:
            logging.warning("item id is not valid 'None' :  {} - 404 ".format(str(id_num)))
            abort(404)


        ##############################    Valid start_time argument   ###########################
        if time_from is None:
            t1 = datetime.datetime.now().strftime("%Y%m"+"01000000")
            logging.warning("query run with default Time ' :  {} - 404 ".format(str(t1)))
        elif Weight.validate(str(time_from)):
            t1 = time_from
        else:
            logging.warning("datetime is not valid ' :  {} - 404 ".format(str(t1)))
            abort(404)
       
        ##############################    Valid end_time  argument   ###########################
        if time_to is None:
            t2 = time_actual
            logging.warning("item id is not valid 'None' :  {} - 404 ".format(str(t2)))
        elif Weight.validate(str(time_to)):
            t2 = time_to
            logging.warning("query run with default Time ' :  {} - 404 ".format(str(t2)))

        else:
            logging.warning("datetime is not valid ' :  {} - 404 ".format(str(t2)))
            abort(404)

 
        ##############################     execute Query       ###########################
        # list to contains Query result
        list_of_session = []

        tara = None
        
        # Query by defualt item is container
        sql_select_Query = "select * from containers_registered where " + \
            "container_id=" + "'" + str(id_num) + "'"
        rows = Connection.Mysql.exec_query(sql_select_Query)


        # if rows isEmpty then check if item is truck  ---- ( if id is not container -> id is truck )
        if not rows:  
            sql_select_Query = "select * from transactions where " + \
                " datetime >= '" + str(t1) + \
                "'and datetime <= '" + str(t2) + "'" + \
                " and truck = " + "'" + str(id_num) + "'"
            rows = Connection.Mysql.exec_query(sql_select_Query)
             
             # rows isEmpty then item not Found
            if not rows:
                logging.warning("item id not Found ' :  {} - 404 ".format(str(id_num)))
                abort(404)
           
           
            ##############################    truck Id      ##############################
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
       


        ##############################    containers Id      ##############################

        container_weight = rows[0][1]
        sql_select_Query = "select * from transactions where " + \
            "datetime >= '" + str(t1) + \
            "' and datetime <= '" + str(t2) + "'"
        
        rows = Connection.Mysql.exec_query(sql_select_Query)
        
        
        if not rows:
            logging.warning("container id not found in transactions Table ' :  {} - 404 ".format(str(id_num)))
            abort(404)

        for row in rows:
            if id_num in str(row[4]).split(','):
                list_of_session.append(row[0])

        item = {
            'id': id_num,
            'tara': container_weight,
            'sessions': list_of_session
        }
        
        logging.warning("item{} - 404 ".format(str(item)))
        return jsonify({'item': item})
