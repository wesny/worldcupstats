import csv
import numpy as np

import spelling_list

class Checker():

    def __init__(self):
        
        #1: Init paths to tables and country list
        pathCC = "./OutputTables/country_constant.csv"
        pathCY = "./OutputTables/country_year.csv"
        pathCL = "./OutputTables/country_list_p.txt"
        pathSP = "./OutputTables/spelling_list.txt"

        #2: Create list of countries
        c_list = genCountryList(pathCL)
        if "Russia" in c_list:
            print "Russia in list"
        checkSpellings(c_list)

        #3: Make sure that country constant contains each country in country list
        f = open(pathCC, 'rb')
        c_not_in_cc = np.ones(len(c_list))
        reader = csv.reader(f)
        for row in reader:
            #print row[0]
            #print c_list == row[0]
            c_not_in_cc[c_list == row[0]] = 0
            #print c_list[c_not_in_cc == 1]
        
        print "Countries not in country constant:{}".format(c_list[c_not_in_cc == 1])

        #4: Make sure that country constant contains each country in country list
        f = open(pathCY, 'rb')
        c_not_in_cy = np.ones(len(c_list))
        reader = csv.reader(f)
        for row in reader:
            #print row[0]
            #print c_list == row[0]
            c_not_in_cy[c_list == row[0]] = 0
            #print c_list[c_not_in_cc == 1]

        print "Countries not in country year:{}".format(c_list[c_not_in_cy == 1])

def genCountryList(pathCL):
    c_list = []

    f = open(pathCL, 'r')
    lines = f.read().split("\n")
    f.close()

    for line in lines:
        print line
        countries = line.split(", ")
        for i in range(len(countries)):
            countries[i] = countries[i].lstrip()
        print countries
        c_list += countries
    c_list = np.array(c_list)

    return c_list

def checkSpellings(c_list):
    
    sp_list = np.array(spelling_list.get_spellings())
    sp_list = sp_list[:,0]
    
    mispelled_list = []
    
    for i in c_list:
        if i not in sp_list:
            mispelled_list.append(i)

    print "Mispelled list:{}".format(mispelled_list)
    

if __name__ == '__main__':
    Checker()
