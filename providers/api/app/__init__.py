from flask import Flask, render_template, redirect, request, Response
app = Flask(__name__)
from app import health, provider, bill, rates, truck

@app.route('/')
def index():
    print("INDEX")
    return render_template("index.html")

