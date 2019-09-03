from flask import Flask, request
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
     subprocess.Popen("./restart.sh")
     return "Yes"