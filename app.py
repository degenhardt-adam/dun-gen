from dungen.dungen import generate
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return generate()
