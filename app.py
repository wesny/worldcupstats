from flask import Flask, render_template, request
from hashlib import sha512
import os
import psycopg2
import urlparse

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

@app.route("/worldcups", methods=['GET', 'POST'])
def world_cup():
	# print('World cup')

	print(request.method)
	if(request.args):

		print(request.args['year'])

		cur.execute("SELECT * FROM worldcup WHERE year = '"+str(request.args['year'])+"';")
		records = cur.fetchall()
		print(records)
		# print(records['winner'])

		if len(records) > 0:
			print('Records')
			records = records[0]
			return render_template("worldcups.html", year=request.args['year'], winner=records[1], runnerup=records[2],third=records[3],fourth=records[4])
		else:
			print('No cup!')
			return render_template("worldcups.html", year=request.args['year'], nocup=True)
	else:
		return render_template("worldcups.html", mystring='whee', myint=1)

if __name__ == '__main__':
    app.run(debug=True)







