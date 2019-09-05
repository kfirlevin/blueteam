import requests
import os
import json
URI = os.environ.get('URI')
def test_bill_get():
<<<<<<< HEAD
    req1 = requests.post(URI+"provider?provider_name=test1")
    assert req1.status_code == 200
    json1 = json.loads(req1.content)
    req = requests.get(URI + 'bill/' + json1['id'])
=======
    req = requests.get(URI + 'bill/5')
    print (req.content)##
>>>>>>> providers
    assert req.status_code == 200