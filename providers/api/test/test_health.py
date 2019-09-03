import requests
import os
URI = os.environ.get('URI')
def test_provider():
    req = requests.get(URI + 'health')
    assert req.status_code == 200