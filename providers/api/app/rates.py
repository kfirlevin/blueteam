from app import app

@app.route('/rates')
def rates():
    return "rates"