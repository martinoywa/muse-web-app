from flask import Flask
from .views import *


app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(signup)
app.register_blueprint(details)
app.register_blueprint(list)
app.register_blueprint(upload)
