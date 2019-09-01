from app import app

@app.route('/truck')
def provider():
    return "truck"