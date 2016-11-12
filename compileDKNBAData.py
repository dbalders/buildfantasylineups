from __future__ import print_function
from nba_py import player
from nba_py import game
import json
import datetime
import os

filename = 'assets/json/data.json'
playerIdList = []
playerSalary = []
playerFantasyPointsAvg = []
finalJson = []
# print(player.get_player('James', 'Michael McAdoo'))
try:
    os.remove(filename)
except OSError:
    pass

with open('assets/json/dkdata.json') as data_file:    
    dkdata = json.load(data_file)

for playerName in dkdata:
	dkPlayerID = 0
	dkPlayerName = playerName['Name'].split(" ", 1)
	dkPlayerFirstName = dkPlayerName[0].replace('.','')
	dkPlayerLastName = dkPlayerName[1]

	print(dkPlayerName)

	if (dkPlayerFirstName == 'JJ' and dkPlayerLastName == 'Barea'):
		dkPlayerFirstName = 'Jose Juan'

	if dkPlayerFirstName == 'DJ':
		dkPlayerFirstName = 'D.J.'

	if dkPlayerFirstName == 'Juancho':
		dkPlayerFirstName = 'Juan'

	if dkPlayerFirstName == 'DeAndre\'':
		dkPlayerFirstName = 'DeAndre'

	if dkPlayerLastName.find('IV') > -1:
		dkPlayerLastName = 'Baldwin'

	if dkPlayerLastName == 'Jones Jr.':
		dkPlayerLastName = 'Jones, Jr.'

	if dkPlayerFirstName == 'Nene':
		dkPlayerID = 2403

	if dkPlayerLastName == 'Robinson III':
		dkPlayerID = 203922

	if dkPlayerLastName == 'Michael McAdoo':
		dkPlayerID = 203949

	if dkPlayerLastName == 'Oubre Jr.':
		dkPlayerID = 1626162

	if dkPlayerLastName == 'Zimmerman Jr.':
		dkPlayerID = 1627757

	if dkPlayerLastName == 'Hernangomez':
		dkPlayerID = 1626195

	if dkPlayerLastName == 'Luwawu-Cabarrot':
		dkPlayerID = 1627789

	if dkPlayerLastName == 'Richard Mbah a Moute':
		dkPlayerID = 201601

	if dkPlayerID == 0:
		dkPlayerID = player.get_player(dkPlayerFirstName, dkPlayerLastName)

	print(dkPlayerID)

	gameLogs = player.PlayerGameLogs(dkPlayerID,'00','2016-17').info()
	# print(gameLogs)

	doubleDouble = False
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
		gamePoints += games['REB'] * 1.25
		gamePoints -= games['TOV'] * .5
		gamePoints += games['FG3M'] * .5
		gamePoints += games['STL'] * 2
		gamePoints += games['BLK'] * 2

		playerGameMinutes += games['MIN']

		gameDate = game.BoxscoreSummary(games['Game_ID']).game_summary()
		gameDate = datetime.datetime.strptime(gameDate[0]['GAME_DATE_EST'], "%Y-%m-%dT%H:%M:%S").date()
		gameDate = str(gameDate.month) + "/" + str(gameDate.day)

		if (games['PTS'] >= 10 and games['AST'] >= 10 and games['REB'] >= 10):
			gamePoints += 3
			doubleDouble = True

		if (games['PTS'] >= 10 and (games['AST'] >= 10 or games['REB'] >= 10 or games['BLK'] >= 10 or games['STL'] >= 10) and doubleDouble == False):
			gamePoints += 1.5
			doubleDouble = True

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

	pointsPerDollar = round(playerName['AvgPointsPerGame'] / (playerName['Salary'] / 1000.0), 1)
	ceilingPPD = round(ceiling / (playerName['Salary'] / 1000.0), 1)
	floorPPD = round(floor / (playerName['Salary'] / 1000.0), 1)

	if len(gameLogs) > 0:
		playerGameMinutes = round(playerGameMinutes / float(len(gameLogs)), 1)

		if len(gameLogs) >= 5:
			lastFiveGamePoints = lastFiveGamePoints / 5.0
			lastFiveGamePointsPPD = round(lastFiveGamePoints / (playerName['Salary'] / 1000.0), 1)
			lastFiveGameMin = lastFiveGameMin / 5.0
		else:
			lastFiveGamePoints = playerName['AvgPointsPerGame']
			lastFiveGamePointsPPD = round(lastFiveGamePoints / (playerName['Salary'] / 1000.0), 1)
			lastFiveGameMin = round(lastFiveGameMin / float(len(gameLogs)), 1)

	finalJson.append({'ID': dkPlayerID, 'Name': playerName['Name'], 'Salary': playerName['Salary'], 'AvgPointsPerGame': playerName['AvgPointsPerGame'], 'PPD': pointsPerDollar, 'MIN': playerGameMinutes, 'Ceiling': ceiling, 'ceilingPPD': ceilingPPD, 'Floor': floor, 'floorPPD': floorPPD, 'lastFivePoints': lastFiveGamePoints, 'lastFivePPD': lastFiveGamePointsPPD, 'lastFiveGameMin':lastFiveGameMin, 'GameLogs': playerGames})

	continue

with open(filename, 'w') as fp:
    json.dump(finalJson, fp)
