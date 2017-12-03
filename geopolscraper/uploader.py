import psycopg2

class Upload():

    def __init__(self):

        #1: Connect to database
        try:
            conn = psycopg2.connect("dbname='worldcupstats_local' user='chris' host='localhost' password='tranquill15'")
            print "Success"
        except:
            print "I am unable to connect to the database"

if __name__ == '__main__':
    Upload()
