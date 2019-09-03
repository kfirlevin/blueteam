import requests
import os
URI = os.environ.get('URI')
def test_provider():
    req = requests.get(URI + 'health')
    if req.status_code == 200:
        return 0
    else:
        return 1