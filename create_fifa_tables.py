import psycopg2
import sys
import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)


def connect():
	host = 'ec2-54-243-48-183.compute-1.amazonaws.com'
	dbname = 'd40e7v3hjfjlmj'
	user = 'lliytjpiskeoot'
	password = 'a6edd34be97a7e235361ab0c611bff0074da3edee95b59813e4729fed881e211'
	conn_string = "host='"+host+"' dbname='"+dbname+"' user='"+user+"' password='"+password+"'"

	conn = psycopg2.connect(conn_string)

	cursor = conn.cursor()

	return conn,cursor


def main():
	conn,cursor = connect()

	cursor.execute("CREATE TABLE country_year (country_name varchar(40), year char(4), matchwins int, matchlosses int, matchdraws int, PRIMARY KEY (country_name, year));")
	cursor.execute("CREATE TABLE country (country_name varchar(40) PRIMARY KEY, cupwins int, matchwins int, matchlosses int, matchdraws int, appearances int);")
	cursor.execute("CREATE TABLE worldcup (year char(4) PRIMARY KEY, winner varchar(40), runner_up varchar(40), third_place varchar(40), fourth_place varchar(40));")

	
	with open('countryyear.csv', 'r') as f:  
		for row in f:
			newrow = '('+row[0:-1]+')'
			cursor.execute("INSERT INTO country_year values "+newrow)

	with open('worldcups.csv','r') as f:
		for row in f:
			newrow = '('+row[0:-1]+')'
			cursor.execute("INSERT INTO worldcup values "+newrow)

	with open('country.csv','r') as f:
		for row in f:
			newrow = '('+row[0:-1]+')'
			cursor.execute("INSERT INTO country values "+newrow)


	cursor.execute("SELECT * FROM country_year WHERE country_name = 'Cameroon';")
	records = cursor.fetchall()
	pprint.pprint(records)

	cursor.execute("SELECT * FROM country WHERE country_name = 'Cameroon';")
	records = cursor.fetchall()
	pprint.pprint(records)

	cursor.execute("SELECT * FROM worldcup WHERE year = '1950';")
	records = cursor.fetchall()
	pprint.pprint(records)
	
	conn.commit()



 
if __name__ == "__main__":
	main()

