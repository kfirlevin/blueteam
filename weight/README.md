# Weight System

## Weight team
- Ahmad
- Kiril
- Moshe
- Nave
---

- The Weighing process (Trucks)
1. Truck enters lot
2. License & Container IDs registered
3. Weight taken (Bruto)
4. Truck unloads containers
5. Weight taken (Truck Tara)

- Import from manufacturer files:
    - CSV
    - Json
- Ad hoc weigh on site

Weight	
	
- [x] Create base flask application
- [x] Create dev docker file 
- [x] GET /health

- [ ] POST /batch-weight  (called by admin) - TODO
    - Open file 
    - convert json to csv function - unic type CSV 
    - reading csv file to list objects 
    - add object to database 
    - implement API use functions  
    - update docker file 
    
- [ ] Test - POST /batch-weight - TODO 
    - testing api
    - testing file (not found / empty)
    - testing add object to db  (no connection / query errors)
    - convert json to csv (check function)
    
- [ ] GET /weight?from=t1&to=t2&filter=f (report by time) -  # DONE - <MOSHI> 
    - - format date
    - insert query & execute it in def func(from,to,filter)
        - default from - day in week
        - default to  - now
        - default filter = “in,out,none”
    - execute query and convert data result to json 
    
    
- [ ] GET/unknown (called by admin) - # DONE - <MOSHI>
    - select where weigth unknown - query 
    - func exec query
    - return json result
    
    
    
- [ ] GET/ item/<id> (truck/container report) 
    - id is for an item (truck or container)
    - 


- [ ] GET /session/<id> (weighing report)   # TODO 
    - Create Session repo (table)
    - write function addSession()
    - GetSessionById()
    - 
- [ ] POST /weight (called by new weight) # TODO 
    - 

![d964392a6d44b5206c153b302c853c7f.png](:/22b85180b5b2493abdea0d2756eea7cf)






Weight System
---
The industrial weight is in charge of weighing trucks, allowing payment to providers.
The WeightApp tracks all weights and allows payment to be for net weight.
(Reminder: Bruto = Neto (fruit) + Tara (truck) + sum(Tara(Containers)))


---
# Services:

## POST /weight
```
- direction=in/out/none
- truck=<license> (If weighing a truck. Otherwise "na")
- containers=str1,str2,... comma delimited list of container ids
- weight=<int>
- unit=kg/lbs {precision is ~5kg, so dropping decimal is a non-issue}
- force=true/false { see logic below }
- produce=<str> { id of produce, e.g. "orange", "tomato", ... OR "na" if enpty}

Records data and server date-time and returns a json object with a unique weight.
Note that "in" & "none" will generate a new session id, and "out" will return session id of previous "in" for the truck.
"in" followed by "in" OR "out" followed by "out":
- if force=false will generate an error
- if force=true will over-write previous weigh of same truck
"out" without an "in" will generate error
"none" after "in" will generate error

Return value on success is:
 { "id": <str>, 
   "truck": <license> or "na",
   "bruto": <int>,
   ONLY for OUT:
   "truckTara": <int>,
   "neto": <int> or "na" // na if some of containers have unknown tara
 }
 ```

## POST /batch-weight
```
- file=<filename>
Will upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers. 
File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
```
https://www.tutorialspoint.com/flask/flask_file_uploading.htm

https://www.w3schools.com/python/python_json.asp

http://blog.appliedinformaticsinc.com/how-to-parse-and-convert-json-to-csv-using-python/

https://www.youtube.com/watch?v=QBq1ScifuaE

https://docs.python.org/3/library/csv.html

```
import pymysql
import codecs
import csv
import urllib2
import pymysql.cursors

# Get URL Data
url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"
URLstream = urllib2.urlopen(url)
csvfile = csv.reader(codecs.iterdecode(URLstream, 'utf-8'))

# Connect to the database

connection = pymysql.connect(host='b8con.no-ip.org', user='HanSolo', password='password', db='EarthQuake', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO quakedata(time, latitude, longitude, depth, mag, magType, nst, gap, dmin, rms, net, id, updated, place, type) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        next(csvfile, None)
        for line in csvfile:
            cursor.execute(sql, (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14]))

finally:
    connection.commit()
    connection.close()
    
```

- upload file function
- convert json to csv function
- reading csv file to list objects 
- add object to database 
- implement API use functions  
- testing 
    - testing api
    - testing upload
    - testing add object to db 
    - convert json to csv
- update docker file 


## GET /unknown

```
Returns a list of all recorded containers that have unknown weight:
["id1","id2",...]
```
- select data 
- https://pynative.com/python-mysql-select-query-to-fetch-data/ 


## GET /weight?from=t1&to=t2&filter=f
```
- t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
- f - comma delimited list of directions. default is "in,out,none"
default t1 is "today at 000000". default t2 is "now". 
returns an array of json objects, one per weighing (batch NOT included):
[{ "id": <id>,
   "direction": in/out/none,
   "bruto": <int>, //in kg
   "neto": <int> or "na" // na if some of containers have unknown tara
   "produce": <str>,
   "containers": [ id1, id2, ...]
},...]
```


[{ "id": <id>,
   "direction": in/out/none,
   "bruto": <int>, //in kg
   "neto": <int> or "na" // na if some of containers have unknown tara
   "produce": <str>,
   "containers": [ id1, id2, ...]
},...]

see : 
https://pynative.com/python-mysql-select-query-to-fetch-data/ 

```
## GET /item/<id>?from=t1&to=t2
```
- id is for an item (truck or container). 404 will be returned if non-existent
- t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
default t1 is "1st of month at 000000". default t2 is "now". 
Returns a json:
{ "id": <str>,
  "tara": <int> OR "na", // for a truck this is the "last known tara"
  "sessions": [ <id1>,...] 
}
```


## GET /session/<id>
```
- id is for a weighing session. 404 will be returned if non-existent
Returns a json:
 { "id": <str>, 
   "truck": <truck-id> or "na",
   "bruto": <int>,
   ONLY for OUT:
   "truckTara": <int>,
   "neto": <int> or "na" // na if some of containers unknown
 }
```
 ## GET /health
 ```
 - By default returns "OK" and status 200 OK
 - If system depends on external resources (e.g. db), and they are not available (e.g. "select 1;" fails ) then it should return "Failure" and 500 Internal Server Error
```

