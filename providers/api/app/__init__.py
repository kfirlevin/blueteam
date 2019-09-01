from flask import Flask

app = Flask(__name__)

from app import health, provider, bill, rates, truck

