from classes import Connection
from flask import  jsonify, abort
import datetime
import csv
import json

class Weight():
    

    def weights_get(time_from, time_to, filter):

        time_actual = datetime.datetime.now().strftime("%Y%m%d%I%M%S")

        if time_from is None:
            t1 = datetime.datetime.now().strftime("%Y%m%d"+"000000")
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
        f = []
        if filter is None:
           f = ["in","out","none"]
        else:
            f = str(filter).split(',')
    
        sql_select_Query = "select * from transactions where " + "datetime>='" + str(t1) + "' and datetime<='" + str(t2) + "'"
        rows =  Connection.Mysql.exec_query(sql_select_Query)

        list_of_transactions = []

        for row in rows:
            if row[2] in f:
                if any(x in str(row[4]).split(',') for x in Weight.unknown_weights()): #na if some of containers have unknown tara
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
            if  not str(row[1]).isdigit():
                list_of_unknown.append(row[0])
        return list_of_unknown

    def batch_weight(fileName):
        flag= False
        ids=[]
        weights=[]
        convert=False
        print(type(fileName))
        print(fileName)
        if fileName.endswith('.csv'):
            try:
                spamReader = csv.reader(open('./in/'+fileName, newline=''), delimiter=',', quotechar='|')
                ids=[]
                weights=[]
                for row in spamReader:
                    ids.append(row[0])
                    weights.append(row[1])
                if str(weights[0]) == '"lbs"':
                    convert=True
                weights.pop(0)
                ids.pop(0)
                flag=True
            except IOError as e: # TODO write to LOGFILE
                print ('I/O error({0}): {1}'.format(e.errno, e.strerror))
                return ('I/O error({0}): {1}'.format(e.errno, e.strerror))

        elif fileName.endswith('.json'):
            try:
                with open('./in/'+fileName) as json_file:
                    data=json.loads(json_file.read())
                if data[1]["unit"]=='lbs':
                    convert = True
                for truck in data:
                    ids.append(truck["id"])
                    weights.append(truck["weight"])
                flag=True
            except IOError as e: # TODO write to LOGFILE
                print ('I/O error({0}): {1}'.format(e.errno, e.strerror))
                return ('I/O error({0}): {1}'.format(e.errno, e.strerror))
              
        if convert:
            for i in range (len(weights)):
                weights[i] = str(int(0.453592*float(weights[i])))
                ids[i]='"' + ids[i] + '"'
        
        for i in range(len(ids)):
            #print("id:"+ids[i]+", weight: "+weights[i])
            #toSend.append("('{}', '{}', 'kg')".format(ids[i], weights[i]))
            query = "INSERT INTO containers_registered(container_id,weight,unit) VALUES(%s,%s,'kg');" % (ids[i],weights[i])
            print(query)
            Connection.Mysql.exec_query(query)
            print(query)
        
        
        if flag:    
            return "OK"
        else: 
            return "Error"

