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


REST

- [ ] POST /weight (called by new weight)
- [ ] POST /batch-weight (called by admin)
- [ ] GET /unknown (called by admin)
- [ ] GET /weight (report by time)
- [ ] GET /item/<id> (truck/container report)
- [ ] GET /session/<id> (weighing report)



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

## GET /unknown

```
Returns a list of all recorded containers that have unknown weight:
["id1","id2",...]
```
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

