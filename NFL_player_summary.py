import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup as bs

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M","N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "Y", "Z"]
letters = ["A"]
# Initialize website and dataframe of player details
website = 'https://www.pro-football-reference.com/'
player_url_list = []
player_from = []
player_to = []
player_name = []
player_position = []
player_weight = []
player_height = []
player_birthdate = []
player_college = []
count = 0
for firstletter in letters:
	url  = 'https://www.pro-football-reference.com/players/'+firstletter+'/'
	html = requests.get(url).content
	soup = bs(html,features="lxml")
	player_count = int(soup.find_all('h2')[1].text.split()[0])
	player_soup = soup.find("div",{"id":"div_players"}).find_all('p')
	for html_tag in player_soup:
		count += 1
		print(count)
		#append player URL for this first letter
		a_tag = html_tag.find('a')
		if a_tag is None:
			continue
		else:
			url = website[:-1] + a_tag['href']
			player_url_list.append(url)
		#append player from and to  for this first letter
		a_tag = html_tag.find('a')
		for i in html_tag.text.split():
			if hasNumbers(i):
				player_from.append(i.split("-")[0])
				player_to.append(i.split("-")[1])
		#access the URL for each player
		html = requests.get(url).content
		soup = bs(html,features="lxml")
		height,weight,birthdate,college,position,name = '','','','','',''
		try:
			#access name
			name = soup.find("h1").text
			#access height
			height = soup.find("span", { "itemprop" : "height" }).text
			height = height.replace("-"," ft ")
			#access weight
			weight = soup.find("span", { "itemprop" : "weight" }).text
			weight = weight[:-2]
			#access birthdate
			birthdate = str(soup.find("span", { "itemprop" : "birthDate" }).text)
			birthdate = birthdate.replace("\xa0"," ")
			birthdate = birthdate.replace("\n","")
			birthdate = birthdate.rstrip()
			#access college
			college = soup.select_one("a[href*=schools]").text
			#access position
			position = str(soup.find_all("p")[1].text.split()[1])
		except:
			pass
		player_name.append(name)
		player_weight.append(weight)
		player_height.append(height)
		player_birthdate.append(birthdate)
		player_college.append(college)
		player_position.append(position)

print(list(map(len,[player_url_list,
                    player_from, 
                    player_to,
                    player_name, 
                    player_position, 
                    player_weight, 
                    player_height, 
                    player_birthdate, 
                    player_college])))

