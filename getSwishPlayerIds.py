# Loads all the player swish id's for quering from the compile

import os
import json
import requests

finalJson = []

swishData = requests.get('https://api.swishanalytics.com/nba/players/fantasy/season?season=2016&apikey=e4d97b074362422b80f18e6545beb37c').json()['data']['results']
playerIds = 'assets/json/swishIds.json'

for players in swishData:
	finalJson.append({'name': players['name'], 'swishID': players['playerId']})

with open(playerIds, 'w') as fp:
    json.dump(finalJson, fp)