from __future__ import print_function
from nba_py import player
from nba_py import game
import json
import datetime
import os

filename = 'assets/json/fdFinalData.json'
playerIdList = []
playerSalary = []
playerFantasyPointsAvg = []
finalJson = []
# print(player.get_player('James', 'Michael McAdoo'))
try:
    os.remove(filename)
except OSError:
    pass

with open('assets/json/fddata.json') as data_file:    
    fddata = json.load(data_file)

for playerName in fddata:
	fdPlayerID = 0
	# dkPlayerName = playerName['Name'].split(" ", 1)
	fdPlayerFirstName = playerName['First Name'].replace('.','')
	fdPlayerLastName = playerName['Last Name']

	print(fdPlayerFirstName + " " + fdPlayerLastName)

	if (fdPlayerFirstName == 'JJ' and fdPlayerLastName == 'Barea'):
		fdPlayerFirstName = 'Jose Juan'

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

	if fdPlayerFirstName == 'Robinson III':
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

	if fdPlayerID == 0:
		fdPlayerID = player.get_player(fdPlayerFirstName, fdPlayerLastName)

	print(fdPlayerID)

	gameLogs = player.PlayerGameLogs(fdPlayerID,'00','2016-17').info()
	# print(gameLogs)

	playerGames = []
	ceiling = 0
	floor = 100
	playerGameMinutes = 0
	lastFive = 0
	lastFiveGamePoints = 0
	lastFiveGamePointsPPD = 0
	lastFiveGameMin = 0

	# print(ceiling)
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
		# print(str(gamePoints) + "points")
		# print(ceiling)
		playerGames.append({'DATE': gameDate, 'MIN': games['MIN'], 'PTS': games['PTS'], 'FG3M': games['FG3M'], 'AST': games['AST'], 'REB': games['REB'], 'STL': games['STL'], 'BLK': games['BLK'], 'TOV': games['TOV'], 'PPD': pointsPerDollarGameLog})

	if floor == 100:
		floor = 0

	pointsPerDollar = round(round(playerName['FPPG'], 1) / (playerName['Salary'] / 1000.0), 1)
	ceilingPPD = round(ceiling / (playerName['Salary'] / 1000.0), 1)
	floorPPD = round(floor / (playerName['Salary'] / 1000.0), 1)

	if len(gameLogs) > 0:
		playerGameMinutes = round(playerGameMinutes / float(len(gameLogs)), 1)

		if len(gameLogs) >= 5:
			print(lastFiveGamePoints)
			lastFiveGamePoints = lastFiveGamePoints / 5.0
			lastFiveGamePointsPPD = round(lastFiveGamePoints / (playerName['Salary'] / 1000.0), 1)
			lastFiveGameMin = lastFiveGameMin / 5.0
			print(lastFiveGamePoints)
		else:
			lastFiveGamePoints = round(playerName['FPPG'], 1)
			lastFiveGamePointsPPD = round(lastFiveGamePoints / (playerName['Salary'] / 1000.0), 1)
			lastFiveGameMin = round(lastFiveGameMin / float(len(gameLogs)), 1)

	print(lastFiveGamePoints)

	finalJson.append({'ID': fdPlayerID, 'Name': fdPlayerFirstName + " " + fdPlayerLastName, 'Salary': playerName['Salary'], 'AvgPointsPerGame': round(playerName['FPPG'], 1), 'PPD': pointsPerDollar, 'MIN': playerGameMinutes, 'Ceiling': round(ceiling, 1), 'ceilingPPD': ceilingPPD, 'Floor': round(floor, 1), 'floorPPD': floorPPD, 'lastFivePoints': round(lastFiveGamePoints, 1), 'lastFivePPD': lastFiveGamePointsPPD, 'lastFiveGameMin':lastFiveGameMin, 'GameLogs': playerGames})

	continue

with open(filename, 'w') as fp:
    json.dump(finalJson, fp)
