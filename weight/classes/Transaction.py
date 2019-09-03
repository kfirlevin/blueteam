class Transaction():

    def transactionToJson(row): 
         return {
             "id": row[0] , 
             "datetime": row[1],
             "direction": row[2],
             "truck": row[3],
             "containers": row[4],
             "bruto": row[5],
             "truckTara": row[6],
             "neto": row[7],
             "produce": row[8] 
            }
    