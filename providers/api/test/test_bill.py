import requests
import os
import json
URI = os.environ.get('URI')
def test_bill_get():
    req = requests.get(URI + 'bill/2')
    print (req.content)
    assert req.status_code == 200