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
    info = json.dumps(request.json)
    temp_branch = info[info.find("refs/heads")+10:info.find("refs/heads")+50]
    branch = temp_branch[1:temp_branch.find("repo")-4]
    if branch == "master":
        subprocess.Popen("./test.sh")
    elif branch == "providers":
        subprocess.Popen("./test2.sh {}".format(branch))
    elif branch == "weight":
        subprocess.Popen("./test2.sh {}".format(branch))
    return "Yes"
