from flask import Flask, escape, request, json
import auto_docker
import health
import time
import sys

sys.stdout.flush()

app = Flask(__name__)

repo_path = '/app/blueteam'

auto_docker.update_repo(repo_path)
auto_docker.activate_docker()
time.sleep(30)
if health.testAPI() == True:
    print("BOKERRRR TOOOOVVV!!!!")
else:
    print('HARA!')


@app.route('/', methods=['POST', 'GET'])
def push():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            auto_docker.update_repo(repo_path)
            auto_docker.activate_docker()
            return json.dumps(request.json)
    elif request.method == 'GET':
        return "This is WebCI"


# @app.route('/commit', methods=['POST', 'GET'])
# def commitLog():
