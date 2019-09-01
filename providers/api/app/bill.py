from app import app

@app.route('/bill')
def bill():
    return "bill"