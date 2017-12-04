import csv
import copy
import numpy as np
from os import listdir
from os.path import isfile, join
import string
import time
import requests

#Downloads raw html from CIA World Factbook to a folder
class CIA_Download():

    def __init__(self):

        CIA_download_folder = "FactbookHTML/"
        
        for country_code in [val1+val2 for val1 in string.lowercase for val2 in string.lowercase]:
    
            url = "https://www.cia.gov/library/publications/the-world-factbook/geos/" + country_code  + ".html"
            r  = requests.get(url)
            time.sleep(0.01)

            if r.status_code == 200:
                d = r.text
                f = open(CIA_download_folder + country_code + ".html", "w")
                f.write(d.encode('utf8'))
                f.close()

#Scrapes raw html in folder
class CIA_Scrape():
    
    def __init__(self):

        CIA_download_path = "./FactbookHTML/"
        outTbl = []

        for filename in [f for f in listdir(CIA_download_path) if isfile(join(CIA_download_path, f))]:
            f = open(CIA_download_path + filename, "r")
            d = f.read().replace('\n', '')
            parsed = Parse_CIA_Country_Data(d)
            if parsed.countryData != None:
                outTbl.append(parsed.countryData)

        #print outTbl

        #Add table headers
        outTbl = [["Country", "Continent", "Land_Area", "Border_Length"]] + outTbl

        #Write table to output
        f = open("./OutputTables/country_constant.csv","w")
        out = csv.writer(f, delimiter=',')
        out.writerows(outTbl)
        f.close()


#Takes a country's data from the CIA World Factbook and parses key statistics from it
class Parse_CIA_Country_Data():

    #: d - block of html from CIA World Factbook
    def __init__(self, d):

        self.countryData = []

        #Find country name
        nameStKey = "<span class=\"region_name1 countryName \">"
        nameEnKey = "</span>"
        name = self.findString(d, nameStKey, nameEnKey).title()

        #Find country continent
        continentStKey = "dark\">"
        continentEnKey = "  <strong>"
        continent = self.findString(d, continentStKey, continentEnKey)

        #Find country land area
        regionKey = "fieldkey=2147"
        stKey = "total: </span><span class=category_data>"
        endKey = " "
        landArea = self.findStringInRegion(d, regionKey, stKey, endKey)
        landArea = landArea.replace(',', '')

        #Find country border length
        regionKey = "Land boundaries:"
        stKey = "total: </span><span class=category_data>"
        enKey = "km"
        borderLength = self.findStringInRegion(d, regionKey, stKey, endKey)
        borderLength = borderLength.replace(',', '')


        #Standardize names
        if name == "Korea, South":
            name = "South Korea"
        elif name == "Korea, North":
            name = "North Korea"
        elif name == "Bosnia And Herzegovina":
            name = "Bosnia and Herzegovina"
        elif name == "Trinidad And Tobago":
            name = "Trinidad and Tobago"
        elif name == "Cote D'Ivoire" or name == "Cote d'Ivoire":
            name = "Ivory Coast"
        elif name == "Congo, Democratic Republic Of The" or name == "Congo, Dem. Rep.":
            name = "Democratic Republic of the Congo"
        elif name == "Bahamas, The":
            name = "Bahamas"

        #Check to see if country is of interest
        pathCL = "./OutputTables/country_list_p.txt"

        f = open(pathCL, 'r')
        lines = f.read().split("\n")
        f.close()

        c_list = []
        for line in lines:
            #print line
            countries = line.split(", ")
            for i in range(len(countries)):
                countries[i] = countries[i].lstrip()
            #print countries
            c_list += countries
        c_list = np.array(c_list)

        if name not in c_list:
            self.countryData = None
            print name
            return

        self.countryData = [name, continent, float(landArea), float(borderLength)]

    def findString(self, d, stKey, endKey):
        strSt = d.find(stKey) + len(stKey)
        strOff = d[strSt:].find(endKey)
        return d[strSt : strSt + strOff]

    def findStringInRegion(self, d, regionKey, stKey, endKey):
        regionSt = d.find(regionKey)
        return self.findString(d[regionSt:], stKey, endKey)

#Reformat world bank data
class Reformat_WB_Data():
    
    def __init__(self):
        
        #Paths to WB Data
        WBFolder = "./WorldBankCVS/"
        GDPFile = "GDP.csv"
        POPFile = "POPULATION.csv"
        LEXFile = "LIFE_EXPECTANCY.csv"
        LITFile = "LITERACY_RATE.csv"
        URBFile = "URBANIZATION.csv"
        paths = [POPFile, LEXFile, URBFile]
        
        outTbl = self.parseCsv(WBFolder + GDPFile)
        for path in paths:
            newTbl = self.parseCsv(WBFolder + path)
            outTbl = self.innerJoin(outTbl, newTbl)

        #Calculate GDP/capita
        for row in outTbl:
            if row[3] != 'NA' and row[4] != 'NA':
                row.append(row[3]/row[4])
            else:
                row.append('NA')

        #Add table headers
        outTbl = [["Country", "Country Code", "Date", "GDP", "Population", "Life Expectancy", "Urbanization Percentage", "Per Capita GDP"]] + \
            outTbl


        #Standardize names
        for i in range(len(outTbl)):
            if outTbl[i][0] == "Egypt, Arab Rep.":
                outTbl[i][0] = "Egypt"
            elif outTbl[i][0] == "Korea, Rep.":
                outTbl[i][0] = "South Korea"
            elif outTbl[i][0] == "Russian Federation":
                outTbl[i][0] = "Russia"
            elif outTbl[i][0] == 'Iran, Islamic Rep.':
                outTbl[i][0] = "Iran"
            elif outTbl[i][0] == 'Slovak Republic':
                outTbl[i][0] = 'Slovakia'
            elif outTbl[i][0] == "Latin America & the Caribbean (IDA & IBRD countries)":
                outTbl[i][0] = "Latin America & the Caribbean"
            elif outTbl[i][0] == "Cote D'Ivoire" or outTbl[i][0] == "Cote d'Ivoire":
                outTbl[i][0] = "Ivory Coast"
            elif outTbl[i][0] == "Congo, Democratic Republic Of The" or outTbl[i][0] == "Congo, Dem. Rep.":
                outTbl[i][0] = "Democratic Republic of the Congo"

                
        #Discard unwanted countries
        pathCL = "./OutputTables/country_list_p.txt"
        c_list = []

        f = open(pathCL, 'r')
        lines = f.read().split("\n")
        f.close()

        for line in lines:
            #print line
            countries = line.split(", ")
            for i in range(len(countries)):
                countries[i] = countries[i].lstrip()
            c_list += countries
        c_list = np.array(c_list)

        prunedTbl = []
        for i in range(len(outTbl)):
            if outTbl[i][0] in c_list:
                prunedTbl.append(outTbl[i])

        #self.printTable(outTbl)
        
        #Write table to output
        f = open("./OutputTables/country_year.csv","w")
        out = csv.writer(f, delimiter=',')
        out.writerows(prunedTbl)
        f.close()

        
            
    #Tables World Bank table, return table of form (Country, Country Code, Year, Datum)
    def parseCsv(self, path):

        #Get CSV
        f = open(path, 'rb')
        reader = csv.reader(f)

        #CSV indicies
        countryI = 0 #Country 
        countryCodeI = 1 #Country code
        startDateI = 4 #Start data index
        headers = None

        #Reformat table
        tbl = []

        for row in reader:

            if headers == None:
                headers = row
                continue

            for i in range(startDateI, len(headers)-1):
                datum = 'NA'
                if row[i] != '':
                    datum = float(row[i])
                tbl.append([row[countryI], row[countryCodeI], headers[i], datum])
        
        f.close()
        return tbl

    def innerJoin(self, t1, t2):
        datumInd = 3
        tbl = []
        for i in range(len(t1)):
            for j in range(2):
                assert t1[i][j] == t2[i][j], "Table rows {}, {} not identical".format(t1[i], t2[i])
            newRow = copy.deepcopy(t1[i])
            newRow.append(t2[i][datumInd])
            tbl.append(newRow)
        return tbl

    def printTable(self, tbl):
        for row in tbl:
            print row

            
if __name__ == '__main__':
    CIA_Scrape()
    Reformat_WB_Data()
