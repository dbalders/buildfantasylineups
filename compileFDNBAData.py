from __future__ import print_function
from nba_py import player
from nba_py import game
from nba_py import team
import json
import datetime
import os
import csv
import urllib2
import requests
import sys

# print(team.TeamSummary(1610612745).info())

paceJson = urllib2.urlopen('http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=')
paceJson = json.loads(paceJson.read())['resultSets'][0]['rowSet']

filename = 'assets/json/fdFinalData.json'
playerIdList = []
playerSalary = []
playerFantasyPointsAvg = []
finalJson = []
numberInList = 0
grinderProj = 0

# if (len(sys.argv) > 1):
# 	if (sys.argv[1] == "today"):
# 		date = str(datetime.date.today())
# else:
# 	date = str(datetime.date.today() + datetime.timedelta(days=1))

grindersProjectionUrl = 'https://rotogrinders.com/projected-stats/nba-player.csv?site=fanduel'
grindersProjectionUrlResponse = urllib2.urlopen(grindersProjectionUrl)
grindersProjData = list(csv.reader(grindersProjectionUrlResponse))

# print(player.get_player('Rivers', 'Austin'))

with open('assets/json/fddata.json') as data_file:    
    fddata = json.load(data_file)
 
with open('assets/json/dvpPG.json') as data_file:    
    dvpPG = json.load(data_file)

with open('assets/json/dvpSG.json') as data_file:    
    dvpSG = json.load(data_file)

with open('assets/json/dvpSF.json') as data_file:    
    dvpSF = json.load(data_file)

with open('assets/json/dvpPF.json') as data_file:    
    dvpPF = json.load(data_file)

with open('assets/json/dvpC.json') as data_file:    
    dvpC = json.load(data_file)

with open('assets/json/teamAbbr.json') as data_file:    
    teamAbbr = json.load(data_file)

for playerName in fddata:
	fdPlayerID = 0
	fdPlayerFullName = str(playerName['First Name']) + " " + str(playerName['Last Name'])
	fdPlayerFirstName = playerName['First Name'].replace('.','')
	fdPlayerLastName = playerName['Last Name']

	numberInList += 1

	print(str(numberInList) + "/" + str(len(fddata)) + " " + fdPlayerFirstName + " " + fdPlayerLastName)

	if (fdPlayerFirstName == 'JJ' and fdPlayerLastName == 'Barea'):
		fdPlayerID = 200826

	if fdPlayerFirstName == 'DJ':
		fdPlayerFirstName = 'D.J.'

	if fdPlayerFirstName == 'Lou':
		fdPlayerFirstName = 'Louis'
		fdPlayerID = 101150

	if fdPlayerLastName == 'Nance Jr.':
		fdPlayerLastName = 'Nance'
		fdPlayerID = 1626204

	if fdPlayerFirstName == 'Juancho':
		fdPlayerFirstName = 'Juan'

	if fdPlayerFirstName == 'DeAndre\'':
		fdPlayerFirstName = 'DeAndre'

	if fdPlayerLastName.find('IV') > -1:
		fdPlayerID = 1627735

	if fdPlayerLastName == 'Jones Jr.':
		fdPlayerLastName = 'Jones, Jr.'

	if fdPlayerLastName == 'Rivers':
		fdPlayerID = 203085

	if fdPlayerFirstName == 'Nene':
		fdPlayerID = 2403

	if fdPlayerLastName == 'Robinson III':
		fdPlayerID = 203922

	if fdPlayerFirstName == 'Michael McAdoo':
		fdPlayerID = 203949

	if fdPlayerLastName == 'Ennis':
		if fdPlayerFirstName == 'James': 
			fdPlayerID = 203516

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

	grindersProj = 0

	for grindersPlayer in grindersProjData:
		if fdPlayerFullName == grindersPlayer[0]:
			grindersProj = grindersPlayer[7]
			break;

	gameLogs = player.PlayerGameLogs(fdPlayerID,'00','2016-17').info()

	for team in teamAbbr:
		if team[0] == playerName['Opponent']:
			oppTeam = team[1]
			if oppTeam == "Los Angeles Clippers":
				oppTeam = "LA Clippers"

		if team[0] == playerName['Team']:
			playerTeam = team[1]

	for pace in paceJson:
		if playerTeam == pace[1]:
			teamPace = pace[19]
		if oppTeam == pace[1]:
			oppPace = pace[19]

	dvpIndex = 0
	if playerName['Position'] == 'PG':
		for team in dvpPG:
			dvpIndex += 1
			if team['team'] == oppTeam:
				break;
				

	if playerName['Position'] == 'SG':
		for team in dvpSG:
			dvpIndex += 1
			if team['team'] == oppTeam:
				break;

	if playerName['Position'] == 'SF':
		for team in dvpSF:
			dvpIndex += 1
			if team['team'] == oppTeam:
				break;

	if playerName['Position'] == 'PF':
		for team in dvpPF:
			dvpIndex += 1
			if team['team'] == oppTeam:
				break;

	if playerName['Position'] == 'C':
		for team in dvpC:
			dvpIndex += 1
			if team['team'] == oppTeam:
				break;

	# print(player.PlayerSummary(fdPlayerID).headline_stats())

	playerGames = []
	lastFive = 0
	lastFiveGamePoints = 0
	lastFiveGamePointsPPD = 0
	lastFiveGameMin = 0

	gameLogCounter = 0

	for games in gameLogs:
		if gameLogCounter < 5:
			gamePoints = 0
			gamePoints += games['PTS']
			gamePoints += games['AST'] * 1.5
			gamePoints += games['REB'] * 1.2
			gamePoints -= games['TOV'] * 1
			gamePoints += games['STL'] * 2
			gamePoints += games['BLK'] * 2

			gameDate = game.BoxscoreSummary(games['Game_ID']).game_summary()
			gameDate = datetime.datetime.strptime(gameDate[0]['GAME_DATE_EST'], "%Y-%m-%dT%H:%M:%S").date()
			gameDate = str(gameDate.month) + "/" + str(gameDate.day)

			pointsPerDollarGameLog = round(gamePoints / (playerName['Salary'] / 1000.0), 1)

			if lastFive < 5:
				lastFiveGamePoints += gamePoints
				lastFiveGameMin += games['MIN']
				lastFive += 1

			playerGames.append({'DATE': gameDate, 'MIN': games['MIN'], 'PTS': games['PTS'], 'FG3M': games['FG3M'], 'AST': games['AST'], 'REB': games['REB'], 'STL': games['STL'], 'BLK': games['BLK'], 'TOV': games['TOV'], 'PPD': pointsPerDollarGameLog})

			gameLogCounter += 1

	pointsPerDollar = round(round(playerName['FPPG'], 1) / (playerName['Salary'] / 1000.0), 1)
	grindersPPD = round(float(grindersProj) / (playerName['Salary'] / 1000.0), 1)

	if len(gameLogs) > 0:
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
		'PPD': pointsPerDollar, 'lastFivePoints': round(lastFiveGamePoints, 1), \
		'lastFivePPD': lastFiveGamePointsPPD, 'lastFiveGameMin':lastFiveGameMin, 'GameLogs': playerGames, \
		'grindersProj': grindersProj, 'grindersPPD': grindersPPD,'oppTeamDvPRank': dvpIndex, 'teamPace': teamPace, 'oppPace': oppPace})
	continue

import optimizer

with open(filename, 'w') as fp:
    json.dump(finalJson, fp)
