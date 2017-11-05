from flask import Flask, render_template
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

# TODO database integration stuff
from models import Country_soccer

@app.route("/")
def home():
    return render_template("test.html")

@app.route("/worldmap")
def world_map():
    return render_template("worldmap.html")

if __name__ == '__main__':
    app.run(debug=True)