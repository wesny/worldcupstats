from os import listdir
from os.path import isfile, join
import string
import time
import requests

#Downloads raw html from CIA World Factbook to a folder
class CIA_Download():

    CIA_download_folder = "FactbookHTML/"
    
    for country_code in [val1+val2 for val1 in string.lowercase for val2 in string.lowercase]:

        url = "https://www.cia.gov/library/publications/the-world-factbook/geos/" + country_code  + ".html"
        #r  = requests.get(url)
        #time.sleep(0.01)

        #if r.status_code == 200:
        #    d = r.text
        #    f = open(CIA_download_folder + country_code + ".html", "w")
        #    f.write(d.encode('utf8'))
        #    f.close()

#Scrapes raw html in folder
class Scrape():
    
    def __init__(self):

        #1: Start by parsing the CIA world factbook for geopolitical data
        CIA_download_path = "./FactbookHTML/"

        for filename in [f for f in listdir(CIA_download_path) if isfile(join(CIA_download_path, f))]:
            f = open(CIA_download_path + filename, "r")
            d = f.read().replace('\n', '')
            ParseCountryData(d)


#Takes a country's data from the CIA World Factbook and parses key statistics from it
class ParseCountryData():

    #: d - block of html from CIA World Factbook
    def __init__(self, d):

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
            return 

        #Find country continent
        continentStKey = "dark\">"
        continentEnKey = "  <strong>"
        continent = self.findString(d, continentStKey, continentEnKey)

        #Find country land area
        regionKey = "fieldkey=2147"
        stKey = "total: </span><span class=category_data>"
        endKey = " "
        area = self.findStringInRegion(d, regionKey, stKey, endKey)

        #Find country border length
        regionKey = "Land boundaries:"
        stKey = "total: </span><span class=category_data>"
        enKey = "km"
        length = self.findStringInRegion(d, regionKey, stKey, endKey)

        print (name, continent, area, length)

    def findString(self, d, stKey, endKey):
        strSt = d.find(stKey) + len(stKey)
        strOff = d[strSt:].find(endKey)
        return d[strSt : strSt + strOff]

    def findStringInRegion(self, d, regionKey, stKey, endKey):
        regionSt = d.find(regionKey)
        return self.findString(d[regionSt:], stKey, endKey)

if __name__ == '__main__':
    Scrape()
