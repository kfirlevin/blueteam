import requests
import os
URI = os.environ.get('URI')
def test_rates_post_bad():
    req = requests.post(URI + 'rates?file=no_such_file.xlsx')
    assert req.status_code == 500
    if req.status_code == 500:
        return 0
    else:
        return 1
def test_rates_post_good():
    req = requests.post(URI + 'rates?file=rates.xlsx')
    assert req.status_code == 200
    if req.status_code == 200:
        return 0
    else:
        return 1
def test_rates_get_good():
    req = requests.get(URI + 'rates')
    assert req.status_code == 200
    if req.status_code == 200:
        return 0
    else:
        return 1