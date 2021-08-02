from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
    return "Home Page"


@app.route("/upload")
def upload():
    return "Upload Page"
