from app import app

@app.route('/provider')
def provider():
    return "provider"