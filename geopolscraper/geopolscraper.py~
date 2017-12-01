import csv
import copy
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

        print outTbl

        #Add table headers
        outTbl = [["Country", "Continent", "Land Area", "BorderLength"]] + outTbl

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

        #Check to see if country is of interest
        excludedCountries = ["Coral Sea Islands", "Baker Island", "French Southern And Antarctic Lands",
                            "Paracel Islands", "Spratly Islands", "United States Pacific Island Wildlife Refuges", 
                            "   World", "Wake Island", "Tokelau", "Svalbard", "Palmyra Atoll", "Midway Islands", 
                            "Niue", "Norfolk Island", "Pitcairn Islands", "Christmas Island", "Kingman Reef", 
                            "South Georgia And South Sandwich Islands", "Johnston Atoll", "Jan Mayen", "Clipperton Island",
                            "Howland Island", "Heard Island And Mcdonald Islands", "Falkland Islands (Islas Malvinas)", "Jarvis Island",
                            "Cocos (Keeling) Islands", "Bouvet Island", "Navassa Island", "Antarctica", "Ashmore And Cartier Islands"]

        if name in excludedCountries or "Ocean" in name:
            self.countryData = None
            return

        #Find country continent
        continentStKey = "dark\">"
        continentEnKey = "  <strong>"
        continent = self.findString(d, continentStKey, continentEnKey)

        #Find country land area
        regionKey = "fieldkey=2147"
        stKey = "total: </span><span class=category_data>"
        endKey = " "
        landArea = self.findStringInRegion(d, regionKey, stKey, endKey)

        #Find country border length
        regionKey = "Land boundaries:"
        stKey = "total: </span><span class=category_data>"
        enKey = "km"
        borderLength = self.findStringInRegion(d, regionKey, stKey, endKey)

        self.countryData = [name, continent, landArea, borderLength]

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

        self.printTable(outTbl)
        
        #Write table to output
        f = open("./OutputTables/country_year.csv","w")
        out = csv.writer(f, delimiter=',')
        out.writerows(outTbl)
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
