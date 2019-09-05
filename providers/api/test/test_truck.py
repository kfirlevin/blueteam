import requests
import os
import json
import random
URI = os.environ.get('URI')
def test_truck_post_good():
    req1 = requests.post(URI + 'provider?provider_name=test11')
    assert req1.status_code == 200
    json1 = json.loads(req1.content)
    req = requests.post(URI + 'truck?provider='+json1['id']+'&id='+str(random.randint(1, 9999999)))
    
    assert req.status_code == 200
def test_truck_post_bad():
    req = requests.post(URI + 'provider?provid_name=test21')
    assert req.status_code != 200
def test_truck_post_bad_2():
    req = requests.post(URI + 'provider?provider_name=test21')
    assert req.status_code == 200
    json1 = json.loads(req.content)
    requests.post(URI + 'truck?provider='+json1['id']+'&id=5')
    req3 = requests.post(URI + 'truck?provider='+json1['id']+'&id=5')
    assert req3.status_code != 200#