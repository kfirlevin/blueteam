from flask import Flask, escape, request, json

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def push():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            return json.dumps(request.json)
    else if request.method == 'GET':
        return "This is WebCI"
