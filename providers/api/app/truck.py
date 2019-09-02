from app import app

@app.route('/truck')
def truck():
    return "truck"