import pandas as pd
import random
import csv
import requests
from bs4 import BeautifulSoup as bs

#initialize website and dataframe of coach details
website = 'https://www.basketball-reference.com/'
html = requests.get(website + "coaches/").content
soup = bs(html)
table = soup.find('table',id='coaches')

#coach names
coaches_html_tags = soup.find_all("th", class_= 'left')
coach_names = []
header_to_remove = ['Coach','Birth Date','College']
for html_tag in coaches_html_tags:
    if html_tag.text in header_to_remove:
        continue
        print("header")
    else:
        coach_names.append(html_tag.text)
    
pandas_coach_names= pd.Series(coach_names)   

# coach links
coach_url_list = []
coaches_html_tags = soup.find_all("th", class_= 'left')
header_to_remove = ['Coach','Birth Date','College']
for html_tag in coaches_html_tags:
    a_tag = html_tag.find('a')
    if a_tag is None:
        continue
    else:
        url = website[:-1] + a_tag['href']
        coach_url_list.append(url)
   
pandas_coach_url_list = pd.Series(coach_url_list)

#coach birthdays
birthdate = soup.select('td[data-stat="birth_date"]')
coach_birth_date = []
for html_tag in birthdate:
    print(html_tag.string)
    coach_birth_date.append(html_tag.string)
pandas_coach_birth_date = pd.Series(coach_birth_date)

#coach college
college = soup.select('td[data-stat="college_name"]')
coach_college = []
for html_tag in college:
    print(html_tag.string)
    coach_college.append(html_tag.string)
pandas_coach_college = pd.Series(coach_college)

#coach from and to
year_min = []
year_max = []
ymin = soup.select('td[data-stat="year_min"]')
ymax = soup.select('td[data-stat="year_max"]')

for html_tag in ymin:
    year_min.append(html_tag.string)
for html_tag in ymax:
    year_max.append(html_tag.string)

pandas_year_min = pd.Series(year_min)
pandas_year_max = pd.Series(year_max)

#consolidation 
coach_list = pd.DataFrame({'Coach':coach_names,'Link':coach_url_list,'From':year_min, 'To':year_max, 'Birth Date':coach_birth_date, 'College':coach_college})

#data check
number_of_coaches = soup.find('h2').string.split(" ")
if int(number_of_coaches[0]) == len(coach_url_list) and len(coach_url_list) != 0:
    print("Same number",len(coach_url_list))

#output
coach_list.to_csv("coach_summary.csv")