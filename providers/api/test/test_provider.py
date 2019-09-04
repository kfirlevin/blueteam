import requests
import os
import json
URI = os.environ.get('URI')
def test_provider_post():
    req = requests.post(URI + 'provider?provider_name=test1')
    assert req.status_code == 200
def test_provider_post_2():
    req = requests.post(URI +'provider?provr_name=test')
    assert req.status_code != 200
def test_provider_put():
    req = requests.post(URI + 'provider?provider_name=test1')
    assert req.status_code == 200
    json1 = json.loads(req.content)
    req2 = requests.put(URI + 'provider/'+json1['id']+'?provider_name=test2')
    assert req2.status_code == 200
def test_provider_put_bad():
    req2 = requests.put(URI + 'provider/7356435636?provider_name=test2')
    assert req2.status_code != 200
