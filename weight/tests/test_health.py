import requests
import pytest


URI = "http://blue.develeap.com:8090"


def test_get_heath():
    response = requests.get(URI + "/health")
    assert response.status_code == 200
