import requests
import pytest


URI = "http://blue.develeap.com:8090"


def test_get_weight():
    response = requests.get(URI + "/weight")
    assert response.status_code == 200


def test_get_weight_with_wrong_from():
    response = requests.get(URI + "/weight?from=1999010101kjsf0101")
    assert response.status_code == 404


def test_get_weight_with_wrong_to():  # add with wrong filter?
    response = requests.get(URI + "/weight?to=1999010101kjsf0101")
    assert response.status_code == 404
