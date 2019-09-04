import requests
import os
import json
URI = os.environ.get('URI')
def test_bill_get():
    req = requests.get(URI + 'bill/5')
    print (req.content)
    assert req.status_code == 200