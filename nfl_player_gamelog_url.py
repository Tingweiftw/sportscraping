import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup as bs
import os

path = "C:\\Users\\fan_t\\Desktop\\ICON\\BACT\\SportsAnalytics\\nfl_player_gamelog_url"
os.chdir(path)

def gethtml (url):
    html = requests.get(url).content
    soup = bs(html,features='lxml')
    return soup

def get_table(url): 
    
    indiv_soup = gethtml(url)
    name = indiv_soup.find("h1").text
    table_stats = bs(str(indiv_soup.find('div', class_ = "overthrow table_container")))
    [allheader] = table_stats.find_all('thead')
    #overheader
    overheader = allheader.find_all('th')
    list_of_overheader = []
    colspan = []
    for tag in overheader:
        try:
            if tag['data-stat']=="ranker":
                break
            else:
                colspan.append([tag.text,tag['colspan']])
                temp_overheaders = [tag.text for i in range(int(tag['colspan']))]
                list_of_overheader += temp_overheaders
        except:
            list_of_overheader+= ['']
    list_of_overheader.pop(0)
    #header
    header = allheader.find_all('th',scope='col')
    list_of_headers = []
    for i in header:
        if i.text != 'Rk':
            list_of_headers.append(i.text)
    #data rows
    data = []
    for tr in table_stats.find_all('tr'):
        row_data = []
        for td in tr.find_all('td'):
            row_data.append(td.text)
        if len(row_data)!=0:
            data.append(row_data)
    for i in range(len(list_of_headers)):
        if list_of_overheader[i]!='':
            list_of_headers[i] = list_of_overheader[i]+'.'+ list_of_headers[i]
    df = pd.DataFrame(data,columns = list_of_headers)
    return [name,df]

letters = ["A","B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M","N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "Y", "Z"]

# Initialize website and dataframe of player details
website = 'https://www.pro-football-reference.com'
gamelog_suburl_list  = []

no_gamelog_list = []
for firstletter in letters:
    if firstletter not in list(os.listdir()):
        os.mkdir(firstletter)
    os.chdir(firstletter)
    soup = gethtml(website+'/players/'+firstletter+'/')
    player_soup = soup.find("div",{"id":"div_players"}).find_all('p')
    for html_tag in player_soup:
        a_tag = html_tag.find('a')
        if a_tag is None:
            continue
        else:
            url = website+a_tag['href'][:-4]+'/gamelog/'
            try:
                datatable = get_table(url)
                datatable[1].to_csv(a_tag['href'][11:-4]+"^"+datatable[0]+".csv",index=False)
            except:
                no_gamelog_list.append(url)
                print(url)