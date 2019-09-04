import requests
import pytest


URI = "http://blue.develeap.com:8090"



def test_get_session():
    response = requests.get(URI + "/session/1")
    assert response.status_code == 200


def test_get_session_with_wrong_id():
    response = requests.get(URI + "/session/1254sdf357212")
    assert response.status_code == 404
