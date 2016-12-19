from bs4 import BeautifulSoup
import urllib2
import json
import os

urls = []

urls.append("http://www.rotowire.com/daily/nba/defense-vspos.htm?pos=PG")
urls.append("http://www.rotowire.com/daily/nba/defense-vspos.htm?pos=SG")
urls.append("http://www.rotowire.com/daily/nba/defense-vspos.htm?pos=SF")
urls.append("http://www.rotowire.com/daily/nba/defense-vspos.htm?pos=PF")
urls.append("http://www.rotowire.com/daily/nba/defense-vspos.htm?pos=C")

for url in urls:
	finalJson = []

	response = urllib2.urlopen(url)
	html = response.read()

	soup = BeautifulSoup(html, 'html.parser')
	rows = soup.find_all("tr")

	headers = {}

	thead = rows[1].find_all('th')

	for i in range(len(thead)):
		headers[i] = thead[i].text.strip().lower()

	del rows[0]
	del rows[0]

	for row in rows:
		# print(row)
		soup2 = BeautifulSoup(str(row), "html.parser")
		soup2 = soup2.find_all("td")

		teamName = "".join(soup2[0].strings)
		position = "".join(soup2[1].strings)
		season = "".join(soup2[2].strings)
		last5 = "".join(soup2[3].strings)
		last10 = "".join(soup2[4].strings)
		# print("".join(soup2[0].strings))
		# print(soup2)
		# soup3 = []
		# cells = row.find_all("td")
		# soup3.append("".join(soup2.strings))
		# print(soup3[0])

		finalJson.append({headers[0]: teamName, headers[1]: position, headers[2]: season, \
			headers[3]: last5, headers[4]: last10})
	# print(json.dumps(data, indent=4))
	    # return soup.findAll('table')
	# get_tables(html)

	# page = urllib.request.urlopen(url).read().decode("utf-8")

	# soup = BeautifulSoup(html, 'html.parser')

	# print(get_tables(html))
	# print(finalJson)

	filename = "assets/json/dvp" + position.upper().rstrip() + ".json"

	with open(filename, 'w') as fp:
	    json.dump(finalJson, fp)