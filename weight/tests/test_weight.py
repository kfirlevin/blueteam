import requests
import os

URI = os.environ.get('URI')


def test_get_weight():
    response = requests.get(URI + "/weight")
    assert response.status_code == 200

def test_get_weight_with_wrong_from():
    response = requests.get(URI + "/weight?from=1999010101kjsf0101")
    assert response.status_code == 404

def test_get_weight_with_wrong_from_2():  
    response = requests.get(URI + "/weight?to=471512")
    assert response.status_code == 404

def test_get_weight_with_wrong_to():  
    response = requests.get(URI + "/weight?to=1999010101kjsf0101")
    assert response.status_code == 404

def test_get_weight_with_wrong_to_2():  
    response = requests.get(URI + "/weight?to=471512")
    assert response.status_code == 404

def test_get_batch_weight():
    response = requests.get(URI + "/batch-weight")
    assert response.status_code == 200

def test_post_batch_weight():
    response = requests.post(URI + "/batch-weight", data={'file': 'containers2.csv'})
    assert response.status_code == 200

def test_post_batch_weight_wrong_file():
    response = requests.post(URI + "/batch-weight", data={'file': 'nghkfn.csv'})
    assert response.status_code == 404