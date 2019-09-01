from app import app

@app.route('/rates')
def provider():
    return "rates"