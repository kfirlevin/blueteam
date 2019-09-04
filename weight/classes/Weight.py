from classes import Connection
from flask import jsonify, abort
import datetime
import csv
import json
import logging


class Weight():

    def validate(date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y%m%d%I%M%S')
        except ValueError:
            return 0
        return 1

    def weights_get(time_from, time_to, filter):

        time_actual = datetime.datetime.now().strftime("%Y%m%d%I%M%S")

        if time_from is None:
            t1 = datetime.datetime.now().strftime("%Y%m%d"+"000000")
        elif Weight.validate(str(time_from)):
            t1 = time_from
        else:
            abort(404)
        if time_to is None:
            t2 = time_actual
        elif Weight.validate(str(time_to)):
            t2 = time_to
        else:
            abort(404)
        f = []
        if filter is None:
            f = ["in", "out", "none"]
        else:
            f = str(filter).split(',')

        sql_select_Query = "select * from transactions where " + \
            "datetime>='" + str(t1) + "' and datetime<='" + str(t2) + "'"
        rows = Connection.Mysql.exec_query(sql_select_Query)

        list_of_transactions = []

        for row in rows:
            if row[2] in f:
                # na if some of containers have unknown tara
                if any(x in str(row[4]).split(',') for x in Weight.unknown_weights()):
                    neto = "na"
                else:
                    neto = row[7]
                transact = {
                    'id': row[0],
                    'direction': row[2],
                    'bruto': row[5],
                    'neto': neto,
                    'produce': row[8],
                    'containers': str(row[4]).split(',')
                }
                list_of_transactions.append(transact)

        return jsonify({'transactions': list_of_transactions})


    def unknown_weights():
        list_of_unknown = []
        sql_select_Query = "select * from containers_registered"
        rows = Connection.Mysql.exec_query(sql_select_Query)

        for row in rows:
            if not str(row[1]).isdigit():
                list_of_unknown.append(row[0])
        return list_of_unknown

    def batch_weight(fileName):
        flag = False
        ids = []
        weights = []
        convert = False
        print(type(fileName))
        print(fileName)
        if fileName.endswith('.csv'):
            try:
                spamReader = csv.reader(
                    open('./in/'+fileName, newline=''), delimiter=',', quotechar='|')
                ids = []
                weights = []
                for row in spamReader:
                    ids.append(row[0])
                    weights.append(row[1])
                if str(weights[0]) == '"lbs"':
                    convert = True
                weights.pop(0)
                ids.pop(0)
                flag = True
            except IOError as e:  # TODO write to LOGFILE
                print('I/O error({0}): {1}'.format(e.errno, e.strerror))
                return ('I/O error({0}): {1}'.format(e.errno, e.strerror)), 404

        elif fileName.endswith('.json'):
            try:
                with open('./in/'+fileName) as json_file:
                    data = json.loads(json_file.read())
                if data[1]["unit"] == 'lbs':
                    convert = True
                for truck in data:
                    ids.append(truck["id"])
                    weights.append(truck["weight"])
                flag = True
            except IOError as e:  # TODO write to LOGFILE
                print('I/O error({0}): {1}'.format(e.errno, e.strerror))
                return ('I/O error({0}): {1}'.format(e.errno, e.strerror)), 404

        if convert:
            for i in range(len(weights)):
                weights[i] = str(int(0.453592*float(weights[i])))
        for i in range(len(ids)):
            ids[i] = '"' + ids[i] + '"'
            #print("id:"+ids[i]+", weight: "+weights[i])
            #toSend.append("('{}', '{}', 'kg')".format(ids[i], weights[i]))
            query = "INSERT INTO containers_registered(container_id,weight,unit) VALUES(%s,%s,'kg');" % (
                ids[i], weights[i])
            print(query)
            Connection.Mysql.exec_query(query)
            print(query)

        if flag:
            return "OK"
        else:
            return "Error", 404


    def container_weight(id_num):
        sql_select_Query = "select * from containers_registered where container_id=" + "'" + id_num + "'"
        rows = Connection.Mysql.exec_query(sql_select_Query)

        if not rows:
            abort(404)
        return str(rows[0][1])

    def last_action(id_num,direction):
        if direction:
            sql_select_Query = "select * from transactions where truck=" + "'" + id_num + "'" + " and direction in " + "('in','out')" + " order by datetime desc limit 1" 
        else:
            sql_select_Query = "select * from transactions where truck=" + "'" + id_num + "'" + " order by datetime desc limit 1" 
        
        rows = Connection.Mysql.exec_query(sql_select_Query)
        if not rows or rows[0][2] == "none":
            return "not found"
            
        return rows[0]

    def all_containers_here(containers_list):
        for id_num in containers_list:
            sql_select_Query = "select * from containers_registered where container_id=" + "'" + id_num + "'"
            rows = Connection.Mysql.exec_query(sql_select_Query)
            if not rows:
                return False

        return True