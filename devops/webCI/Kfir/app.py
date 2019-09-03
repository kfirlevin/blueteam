from flask import Flask, request
import subprocess
app = Flask(__name__)

@app.route('/upload')
def restart():
        subprocess.Popen("./prod-up.sh")
        return "Up"

@app.route('/webhook', methods=['POST'])
def run_testing_env():
    if request.headers['X-GitHub-Event'] == 'push':
#run bash script that creating the test env using the command:
# subprocess.call("path/to/script", shell=True) 
#then run yanay checks - if they true, upload to prod,else none
        return 0

#Note - if we want to make a switch without downtime we need to use nginx