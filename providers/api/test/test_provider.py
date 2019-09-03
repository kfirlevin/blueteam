import requests
import os
URI = os.environ.get('URI')
def test_provider_post():
    req = requests.post(URI + 'provider?provider_name=test1')
    assert req.status_code == 200
    if req.status_code == 200:
        return 0
    else:
        return 1
def test_provider_post_2():
    req = requests.post(URI +'provider?provr_name=test')
    print(req.status_code)
    assert req.status_code != 200
    if req.status_code == 200:
        return 1
    else:
        return 0