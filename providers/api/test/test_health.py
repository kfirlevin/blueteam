import requests
def test_health():
    req = requests.get('http://localhost:8010/health')
    if req.status_code == 200:
        return 0
    else:
        return 1