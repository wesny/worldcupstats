from flask import Flask, render_template
from hashlib import sha512
import os
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = sha512("cybersec".encode('utf-8')).hexdigest()
app.config['TEMPLATES_AUTO_RELOAD'] = True

url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = psycopg2.connect(db)
cur = conn.cursor()

env = app.jinja_env
env.line_statement_prefix = '='

@app.route("/")
def home():
    return render_template("test.html")

@app.route("/worldmap")
def world_map():
    return render_template("worldmap.html")

if __name__ == '__main__':
    app.run(debug=True)