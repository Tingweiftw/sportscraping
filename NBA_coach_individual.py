import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup as bs
from bs4 import Comment
import os


def get_coaching_record(tempsoup):
	coaching_record = {}
	thcolnames = ['season']
	tdcolnames = ['age','lg_id','team_id','g','wins','losses','win_loss_pct','wins_over_500','rank_team','g_playoffs','losses_playoffs','win_loss_pct_playoffs','coach_remarks','role']

	coaching_record['season'] = []
	for i in tdcolnames:
	    coaching_record[i] = []
	try:
		[coaching_record_table] = tempsoup.findAll('tbody')
		for i in coaching_record_table.findAll('tr'):
		    temp1 = i.select('th[data-stat="season"]')[0].text
		    #print(temp1)
		    coaching_record["season"].append(temp1)
		    for j in tdcolnames:
		        try:
		            temp2 = i.select('td[data-stat="'+j+'"]')[0].text
		            
		            if temp2 == '':
		                coaching_record[j].append('NIL')
		            else:
		                coaching_record[j].append(temp2)
		        except:
		            #print("No ",j," in this row")
		            coaching_record[j].append("NIL")
		pandas_coaching_record = pd.DataFrame.from_dict(coaching_record)
		return pandas_coaching_record
	except:
		return None

def get_coaching_award(tempsoup):
	try:
		comment = tempsoup.find_all(text=lambda text: isinstance(text, Comment))
		for i in comment:
		    if "<tbody>" in str(i):
		        award = bs(i)
		list_season,list_award_id,list_league = [],[],[]
		for i in award.select("tr"):
		    try:
		        season = i.select('th[data-stat="season"]')[0]
		        award_id = i.select('td[data-stat="award_id"]')[0]
		        league = i.select('a')[0]
		        list_season.append(season.text)
		        list_award_id.append(award_id.text)
		        list_league.append(league.text)
		    except:
		        continue
		pandas_coaching_award = pd.DataFrame({'Season':list_season,'League':list_league,'Award':list_award_id})
		return pandas_coaching_award
	except:
		return None

def get_coaching_transaction(tempsoup):
	try:
		coaching_transaction_table = tempsoup.find_all('table')[1]
		# coaching_transaction_table
		list_date, list_detail = [],[]
		for i in coaching_transaction_table:
		    try:
		        if 'Transactions Table' not in i:
		            temp = i.text.split(":")
		            list_date.append(temp[0])
		            list_detail.append(temp[1])
		        else:
		            continue
		    except:
		        continue     
		pandas_coaching_award = pd.DataFrame({'Date':list_date,'Details':list_detail})
		return pandas_coaching_award
	except:
		return None

#initialize website and dataframe of coach details
website = 'https://www.basketball-reference.com/'
html = requests.get(website + "coaches/").content
soup = bs(html)
# Empty List
coach_url_list = []
# Look for the table with coaches
coaches_html_tags = soup.find_all("th", class_= 'left')

header_to_remove = ['Coach','Birth Date','College']

#coach url
for html_tag in coaches_html_tags:
    a_tag = html_tag.find('a')
    if a_tag is None:
        continue
    else:
        url = website[:-1] + a_tag['href']
        coach_url_list.append(url)
path="C:\\Users\\fan_t\\Desktop\\BACT\\SportsAnalytics\\coach_individual"
os.chdir(path)
count = 0
for individual_link in coach_url_list:
	html = requests.get(individual_link).content
	coach_soup = bs(html)
	coach_name = coach_soup.find("h1").text
	coach_name = coach_name.replace(" ","_")
	newpath = "C:\\Users\\fan_t\\Desktop\\BACT\\SportsAnalytics\\coach_individual\\"+coach_name
	if not os.path.exists(newpath):
		os.makedirs(newpath)
		os.chdir(newpath)
	try:
		get_coaching_record(coach_soup).to_csv(coach_name+"_Record.csv",index=False)
		get_coaching_transaction(coach_soup).to_csv(coach_name+"_Transaction.csv",index=False)
		get_coaching_award(coach_soup).to_csv(coach_name+"_Award.csv",index=False)
	except:
		print("Missing Table")
	count +=1
	print("done with: ",count," coaches")

