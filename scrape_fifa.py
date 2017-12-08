from bs4 import BeautifulSoup
import requests
import re
import pprint


pp = pprint.PrettyPrinter(indent=4)
r = requests.get('http://www.fifa.com/fifa-tournaments/archive/worldcup/index.html')
data = r.text
soup = BeautifulSoup(data, "lxml")
worldcups = {}
countryDict = {}
countryYearDict = {}

li = soup.find_all('li', {'class': 'comp-item'})

for item in li:
	worldcup = requests.get('http://www.fifa.com'+item.find('a')['href'])
	data = worldcup.text

	year = item.find('a')['href'].split('/')
	year = year[3][len(year[3])-4:]

	yearDict = {}

	soup = BeautifulSoup(data, "lxml")

	winner = soup.find_all('div', {'class':'c-team-rank'})

	ranks = winner[0].find_all('span', {'class':'t-nText'})
	
	countryRanks = []
	for rank in ranks:
		countryRanks.append(rank.find('a').getText())
	cupWinner = countryRanks[0]
	yearDict['winner'] = countryRanks[0]
	yearDict['runnerUp'] = countryRanks[1]
	yearDict['third'] = countryRanks[2]
	yearDict['fourth'] = countryRanks[3]

	worldcups[year] = yearDict

	matches = requests.get('http://www.fifa.com'+soup.find('a', {'title':'Matches'})['href'])

	data = matches.text
	soup = BeautifulSoup(data, "lxml")

	end = False
	matchList = soup.find_all('div', {'class':'mu result'})

	appearances = {}
	for match in matchList:
		teams = match.find_all('span',{'class':'t-nText'})
		score = match.find_all('span',{'class':'s-scoreText'})[0].text.split('-')
		
		appearances[teams[0].text] = True
		appearances[teams[1].text] = True
		
		if teams[0].text not in countryDict:
			countryDict[teams[0].text] = {}
			countryDict[teams[0].text]['matchWins'] = 0
			countryDict[teams[0].text]['matchLosses'] = 0
			countryDict[teams[0].text]['matchTies'] = 0
			countryDict[teams[0].text]['cupWins'] = 0
			countryDict[teams[0].text]['appearances'] = 0
		if teams[1].text not in countryDict:
			countryDict[teams[1].text] = {}
			countryDict[teams[1].text]['matchWins'] = 0
			countryDict[teams[1].text]['matchLosses'] = 0
			countryDict[teams[1].text]['matchTies'] = 0
			countryDict[teams[1].text]['cupWins'] = 0
			countryDict[teams[1].text]['appearances'] = 0


		if (teams[0].text,year) not in countryYearDict:
			countryYearDict[(teams[0].text,year)] = {}
			countryYearDict[(teams[0].text,year)]['matchWins'] = 0
			countryYearDict[(teams[0].text,year)]['matchLosses'] = 0
			countryYearDict[(teams[0].text,year)]['matchTies'] = 0
		if (teams[1].text,year) not in countryYearDict:
			countryYearDict[(teams[1].text,year)] = {}
			countryYearDict[(teams[1].text,year)]['matchWins'] = 0
			countryYearDict[(teams[1].text,year)]['matchLosses'] = 0
			countryYearDict[(teams[1].text,year)]['matchTies'] = 0


		if score[0] == score[1]:
			winner = False
		else:
			if int(score[0]) > int(score[1]):
				winner = teams[0].text
				runnerUp = teams[1].text
			else:
				winner = teams[1].text
				runnerUp = teams[0].text
		if winner:
			countryDict[winner]['matchWins'] += 1
			countryDict[runnerUp]['matchLosses'] += 1

			countryYearDict[(winner,year)]['matchWins'] += 1
			countryYearDict[(runnerUp,year)]['matchLosses'] += 1
		else:
			countryDict[teams[0].text]['matchTies'] += 1
			countryDict[teams[1].text]['matchTies'] += 1

			countryYearDict[(teams[0].text,year)]['matchTies'] += 1
			countryYearDict[(teams[1].text,year)]['matchTies'] += 1

	countryDict[cupWinner]['cupWins'] += 1
	for key in appearances:
		countryDict[key]['appearances'] += 1

with open('worldcups.csv','w') as file:
	for key in worldcups:
		print(key)
		line = "'"+key+"', '"+worldcups[key]['winner']+"', '"+worldcups[key]['runnerUp']+"', '"+worldcups[key]['third']+"', '"+worldcups[key]['fourth']+"'"
		file.write(line)
		file.write('\n')
		
with open('country.csv','w') as file:
	for key in countryDict:
		if key == "CÃ´te d'Ivoire":
			country = "Ivory Coast"
		else:
			country = key
		print(key)
		line = "'"+country+"', "+str(countryDict[key]['cupWins'])+", "+str(countryDict[key]['matchWins'])+", "+str(countryDict[key]['matchLosses'])+", "+str(countryDict[key]['matchTies'])+", "+str(countryDict[key]['appearances'])
		file.write(line)
		file.write('\n')

with open('countryyear.csv','w') as file:
	for key in countryYearDict:
		if key[0] == "CÃ´te d'Ivoire":
			country = "Ivory Coast"
		else:
			country = key[0]
		print(key)
		line = "'"+country+"', '"+key[1]+"', "+str(countryYearDict[key]['matchWins'])+", "+str(countryYearDict[key]['matchLosses'])+', '+str(countryYearDict[key]['matchTies'])
		file.write(line)
		file.write('\n')







