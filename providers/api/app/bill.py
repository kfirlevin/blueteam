from app import app

@app.route('/bill')
def health():
    return "bill"