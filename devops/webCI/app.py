from flask import Flask, request, json
import subprocess
app = Flask(__name__)


@app.route('/up')
def up():
    subprocess.Popen("./prod-up.sh")
    return "Up"


@app.route('/down')
def down():
    subprocess.Popen("./prod-down.sh")
    return "Down"


@app.route('/webhook', methods=['POST'])
def run_testing_env():
    shuki = request.get_json()
    print shuki
    branch = shuki['ref'].split('/')[2]
    if shuki['ref'].split('/')[2] == "master":
        subprocess.Popen("./test.sh")
    elif branch == "providers":
        subprocess.Popen("./test2.sh")
    elif branch == "weight":
        subprocess.Popen("/test3.sh")
    return "Yes"
