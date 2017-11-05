from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha512
import os

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = sha512("cybersec".encode('utf-8')).hexdigest()
app.config['TEMPLATES_AUTO_RELOAD'] = True

env = app.jinja_env
env.line_statement_prefix = '='

from models import Country_soccer

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)