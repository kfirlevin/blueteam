import requests
import os

URI = os.environ.get('URI')


def test_get_heath():
    response = requests.get(URI + "/health")
    assert response.status_code == 200
