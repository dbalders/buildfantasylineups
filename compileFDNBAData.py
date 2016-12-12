from __future__ import print_function
from nba_py import player
from nba_py import game
import json
import datetime
import os
import csv
import urllib2
import requests

filename = 'assets/json/fdFinalData.json'
playerIdList = []
playerSalary = []
playerFantasyPointsAvg = []
finalJson = []
numberInList = 0
tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
grinderProj = 0
swishProj = 0

grindersProjectionUrl = 'https://rotogrinders.com/projected-stats/nba-player.csv?site=fanduel'
grindersProjectionUrlResponse = urllib2.urlopen(grindersProjectionUrl)
grindersProjData = list(csv.reader(grindersProjectionUrlResponse))
swishProjData = requests.get('https://api.swishanalytics.com/nba/players/fantasy?date=' + tomorrow + '/&apikey=e4d97b074362422b80f18e6545beb37c').json()['data']['results']

# print(player.get_player('James', 'Michael McAdoo'))

with open('assets/json/fddata.json') as data_file:    
    fddata = json.load(data_file)

with open('assets/json/swishIds.json') as data_file:    
    swishIds = json.load(data_file)
 
for playerName in fddata:
	fdPlayerID = 0
	fdPlayerFullName = str(playerName['First Name']) + " " + str(playerName['Last Name'])
	fdPlayerFirstName = playerName['First Name'].replace('.','')
	fdPlayerLastName = playerName['Last Name']

	numberInList += 1

	print(str(numberInList) + "/" + str(len(fddata)) + " " + fdPlayerLastName)

	if (fdPlayerFirstName == 'JJ' and fdPlayerLastName == 'Barea'):
		fdPlayerID = 200826

	if fdPlayerFirstName == 'DJ':
		fdPlayerFirstName = 'D.J.'

	if fdPlayerFirstName == 'Juancho':
		fdPlayerFirstName = 'Juan'

	if fdPlayerFirstName == 'DeAndre\'':
		fdPlayerFirstName = 'DeAndre'

	if fdPlayerLastName.find('IV') > -1:
		fdPlayerLastName = 'Baldwin'

	if fdPlayerLastName == 'Jones Jr.':
		fdPlayerLastName = 'Jones, Jr.'

	if fdPlayerFirstName == 'Nene':
		fdPlayerID = 2403

	if fdPlayerLastName == 'Robinson III':
		fdPlayerID = 203922

	if fdPlayerFirstName == 'Michael McAdoo':
		fdPlayerID = 203949

	if fdPlayerLastName == 'Oubre Jr.':
		fdPlayerID = 1626162

	if fdPlayerLastName == 'Zimmerman Jr.':
		fdPlayerID = 1627757

	if fdPlayerLastName == 'Hernangomez':
		fdPlayerID = 1626195

	if fdPlayerLastName == 'Luwawu-Cabarrot':
		fdPlayerID = 1627789

	if fdPlayerLastName == 'Richard Mbah a Moute':
		fdPlayerID = 201601

	if fdPlayerLastName == 'Mbah a Moute':
		fdPlayerID = 201601

	if fdPlayerLastName == 'Tavares':
		fdPlayerID = 204002

	if fdPlayerLastName == 'Bembry':
		fdPlayerID = 1627761

	if fdPlayerID == 0:
		fdPlayerID = player.get_player(fdPlayerFirstName, fdPlayerLastName)

	foundSwishID = 'false'

	for swishPlayer in swishIds:
		if fdPlayerFullName == swishPlayer['name']:
			foundSwishID = 'true'
			fdPlayerSwishId = swishPlayer['swishID']
			break;

	if foundSwishID == 'false':
		print(fdPlayerFullName + " ERROR SWISH ID NOT FOUND")

	grindersProj = 0

	for grindersPlayer in grindersProjData:
		if fdPlayerFullName == grindersPlayer[0]:
			grindersProj = grindersPlayer[7]
			break;

	swishProj = 0

	for swishPlayer in swishProjData:
		if fdPlayerFullName == swishPlayer['name']:
			swishProj = swishPlayer['fanduelFpts']
			break;


	gameLogs = player.PlayerGameLogs(fdPlayerID,'00','2016-17').info()

	playerGames = []
	ceiling = 0
	floor = 100
	playerGameMinutes = 0
	lastFive = 0
	lastFiveGamePoints = 0
	lastFiveGamePointsPPD = 0
	lastFiveGameMin = 0

	for games in gameLogs:
		gamePoints = 0
		gamePoints += games['PTS']
		gamePoints += games['AST'] * 1.5
		gamePoints += games['REB'] * 1.2
		gamePoints -= games['TOV'] * 1
		gamePoints += games['STL'] * 2
		gamePoints += games['BLK'] * 2

		playerGameMinutes += games['MIN']

		gameDate = game.BoxscoreSummary(games['Game_ID']).game_summary()
		gameDate = datetime.datetime.strptime(gameDate[0]['GAME_DATE_EST'], "%Y-%m-%dT%H:%M:%S").date()
		gameDate = str(gameDate.month) + "/" + str(gameDate.day)

		if gamePoints > ceiling:
			ceiling = gamePoints

		if gamePoints < floor:
			floor = gamePoints

		pointsPerDollarGameLog = round(gamePoints / (playerName['Salary'] / 1000.0), 1)

		if lastFive < 5:
			lastFiveGamePoints += gamePoints
			lastFiveGameMin += games['MIN']
			lastFive += 1

		playerGames.append({'DATE': gameDate, 'MIN': games['MIN'], 'PTS': games['PTS'], 'FG3M': games['FG3M'], 'AST': games['AST'], 'REB': games['REB'], 'STL': games['STL'], 'BLK': games['BLK'], 'TOV': games['TOV'], 'PPD': pointsPerDollarGameLog})

	if floor == 100:
		floor = 0

	pointsPerDollar = round(round(playerName['FPPG'], 1) / (playerName['Salary'] / 1000.0), 1)
	ceilingPPD = round(ceiling / (playerName['Salary'] / 1000.0), 1)
	floorPPD = round(floor / (playerName['Salary'] / 1000.0), 1)
	grindersPPD = round(float(grindersProj) / (playerName['Salary'] / 1000.0), 1)
	swishPPD = round(float(swishProj) / (playerName['Salary'] / 1000.0), 1)

	if len(gameLogs) > 0:
		playerGameMinutes = round(playerGameMinutes / float(len(gameLogs)), 1)

		if len(gameLogs) >= 5:
			lastFiveGamePoints = lastFiveGamePoints / 5.0
			lastFiveGamePointsPPD = round(lastFiveGamePoints / (playerName['Salary'] / 1000.0), 1)
			lastFiveGameMin = lastFiveGameMin / 5.0
		else:
			lastFiveGamePoints = round(playerName['FPPG'], 1)
			lastFiveGamePointsPPD = round(lastFiveGamePoints / (playerName['Salary'] / 1000.0), 1)
			lastFiveGameMin = round(lastFiveGameMin / float(len(gameLogs)), 1)

	finalJson.append({'ID': fdPlayerID, 'Name': fdPlayerFirstName + " " + fdPlayerLastName, 'Salary': playerName['Salary'], \
		'Position': playerName['Position'], 'Team': playerName['Team'], 'AvgPointsPerGame': round(playerName['FPPG'], 1), \
		'PPD': pointsPerDollar, 'MIN': playerGameMinutes, 'Ceiling': round(ceiling, 1), 'ceilingPPD': ceilingPPD, \
		'Floor': round(floor, 1), 'floorPPD': floorPPD, 'lastFivePoints': round(lastFiveGamePoints, 1), \
		'lastFivePPD': lastFiveGamePointsPPD, 'lastFiveGameMin':lastFiveGameMin, 'GameLogs': playerGames, \
		'grindersProj': grindersProj, 'grindersPPD': grindersPPD, 'swishProj': swishProj, 'swishPPD': swishPPD, 'swishID': fdPlayerSwishId})
	continue

import optimizer

with open(filename, 'w') as fp:
    json.dump(finalJson, fp)
