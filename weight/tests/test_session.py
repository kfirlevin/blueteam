import requests
import pytest


URI = "http://blue.develeap.com:8090"

def test_get_weight():
    response = requests.get(URI + "/weight")
    assert response.status_code == 200

def test_get_weight_with_wrong_from():
    response = requests.get(URI + "/weight?from=1999010101kjsf0101")
    assert response.status_code == 404

def test_get_weight_with_wrong_to():             #add with wrong filter?
    response = requests.get(URI + "/weight?to=1999010101kjsf0101")
    assert response.status_code == 404

def test_get_heath():
    response = requests.get(URI + "/health")
    assert response.status_code == 200

def test_get_item():
    response = requests.get(URI + "/item/T-123523?from=19990101010101")
    assert response.status_code == 200

def test_get_item_with_wrong_from():
    response = requests.get(URI + "/item/T-123523?from=skjdf")
    assert response.status_code == 404

def test_get_item_with_wrong_id():
    response = requests.get(URI + "/item/T-15kjhj23?from=19990101010101")
    assert response.status_code == 404

def test_get_item_with_wrong_to():
    response = requests.get(URI + "/item/T-123523?to=sdkjfsdn")
    assert response.status_code == 404

def test_get_session():
    response = requests.get(URI + "/session/1")
    assert response.status_code == 200

def test_get_session_with_wrong_id():
    response = requests.get(URI + "/session/1254sdf357212")
    assert response.status_code == 404


