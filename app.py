from flask import Flask, render_template, request
from hashlib import sha512
import os
import psycopg2
import urlparse
import pprint
import json

app = Flask(__name__)
app.secret_key = sha512("cybersec".encode('utf-8')).hexdigest()
app.config['TEMPLATES_AUTO_RELOAD'] = True

url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = psycopg2.connect(db)
cur = conn.cursor()

env = app.jinja_env
env.line_statement_prefix = '='

cup_years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014]

@app.route("/")
def home():
    d = create_graph_data("Germany")
    return render_template("country_table.html", d=d)

@app.route("/worldmap")
def world_map():
    return render_template("worldmap.html")

@app.route("/worldcups")
def world_cup():
    # print('World cup')

    if(request.args):

        print(request.args['year'])

        cur.execute("SELECT * FROM worldcup WHERE year = '"+str(request.args['year'])+"';")
        records = cur.fetchall()
        
        if len(records) > 0:
            print('Records')
            records = records[0]
            return render_template("worldcups.html", year=request.args['year'], winner=records[1], runnerup=records[2],third=records[3],fourth=records[4])
        else:
            print('No cup!')
            return render_template("worldcups.html", year=request.args['year'], nocup=True)
    else:
        return render_template("worldcups.html")

@app.route("/wins_year")
def wins_year():
    if(request.args):
        if request.args['country'] and request.args['year']:
            records = get_wins_year(request.args['country'], request.args['year'])
            return render_template("wins.html", year=request.args['year'], country=request.args['country'], records=records)
        elif request.args['country']:
            records = get_wins_year(request.args['country'], 0)
            return render_template("wins.html", year='', country=request.args['country'], records=records)
        elif request.args['year']:
            records = get_wins_year(0, request.args['year'])
            return render_template("wins.html", year=request.args['year'], country='', records=records)
        else:
            records = get_wins_year(0,0)
            return render_template("wins.html",year='', country='', records=records)
    else:
        records = get_wins_year(0,0)
        return render_template("wins.html",year='', country='', records=records)


def get_wins_year(country=False,year=False):
    if year and country:
        cur.execute("SELECT * FROM country_year where year='"+year+"' and country_name='"+country+"';")
        records = cur.fetchall()
        return records
    elif country:
        cur.execute("SELECT * FROM country_year where country_name='"+country+"' ORDER BY year;")
        records = cur.fetchall()
        return records
    elif year:
        cur.execute("SELECT * FROM country_year where year='"+year+"' ORDER BY country_name;")
        records = cur.fetchall()
        return records
    else:
        cur.execute("SELECT * FROM country_year ORDER BY country_name, year;")
        records = cur.fetchall()
        return records

def create_graph_data(country):
    wins_by_year = []
    wins_db_res = get_wins_year(country)
    i = 0
    j = 0
    while i < len(cup_years):
        if j < len(wins_db_res) and cup_years[i] == int(wins_db_res[j][1]):
            wins_by_year.append(wins_db_res[j][2])
            i += 1
            j += 1
        else:
            wins_by_year.append(0)
            i += 1
    ret_d = {}
    ret_d['years'] = cup_years
    ret_d['wins'] = wins_by_year
    ret_d['country'] = country
    capita_gdp_db = get_stats(country)
    per_capita_gdp = []
    i = 0
    j = 0
    while i < len(cup_years):
        if j < len(capita_gdp_db) and cup_years[i] == int(capita_gdp_db[j][2]):
            per_capita_gdp.append(capita_gdp_db[j][7])
            i += 1
            j += 1
        else:
            per_capita_gdp.append(None)
            i += 1
    ret_d['per_capita_gdp'] = json.dumps(per_capita_gdp)
    return ret_d

@app.route("/wins_overall")
def wins_overall():
    if(request.args):
        if request.args['country']:
            records = get_wins_overall(request.args['country'])
            return render_template("wins.html", country=request.args['country'], records=records)
        else:
            records = get_wins_overall(0)
            return render_template("wins_overall.html",country='', records=records)
    else:
        records = get_wins_overall(0)
        return render_template("wins_overall.html",country='', records=records)     

def get_wins_overall(country):
    if country:
        cur.execute("SELECT * FROM country where country_name='"+country+"';")
        records = cur.fetchall()
        return records
    else:
        cur.execute("SELECT * FROM country ORDER BY country_name;")
        records = cur.fetchall()
        return records

def get_stats(country):
    cur.execute("SELECT * FROM country_year_geopol where country='"+country+"' and year in"+str(tuple(cup_years))+" ORDER BY year;")
    records = cur.fetchall()
    return records
    
if __name__ == '__main__':
    app.run(debug=True)







