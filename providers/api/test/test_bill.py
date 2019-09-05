import requests
import os
import json
URI = os.environ.get('URI')
def test_bill_get():
    req1 = requests.post(URI+"provider?provider_name=test1")
    assert req1.status_code == 200
    json1 = json.loads(req1.content)
    req = requests.get(URI + 'bill/' + json1['id'])
    assert req.status_code == 200
def test_bill_get_bad():
    req = requests.get(URI + 'bill/883726')
    assert req.status_code != 200