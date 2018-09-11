import pandas as pd
import csv
import os
import re
import requests
from bs4 import BeautifulSoup as bs

#initialize website and dataframe of coach details
website = 'https://www.basketball-reference.com/'
html = requests.get(website + "coaches/").content
soup = bs(html)
table = soup.find('table',id='coaches')

# Get coach names
coaches_html_tags = soup.find_all("th", class_= 'left')
coach_names = []
header_to_remove = ['Coach','Birth Date','College']
for html_tag in coaches_html_tags:
    if html_tag.text in header_to_remove:
        continue
        print("header")
    else:
        coach_names.append(html_tag.text)

# Get coach links
coaches_html_tags = soup.find_all("th", class_= 'left')
coach_url_list = []
header_to_remove = ['Coach','Birth Date','College']
for html_tag in coaches_html_tags:
    a_tag = html_tag.find('a')
    if a_tag is None:
        continue
    else:
        url = website[:-1] + a_tag['href']
        coach_url_list.append(url)

# Get coach birth dates
birthdate = soup.select('td[data-stat="birth_date"]')
coach_birth_date = []
for html_tag in birthdate:
    coach_birth_date.append(html_tag.string)


# Get list of college of coach
college = soup.select('td[data-stat="college_name"]')
coach_college = []
for html_tag in college:
    coach_college.append(html_tag.string)

# Get "From" and "To"
year_min = []
year_max = []
ymin = soup.select('td[data-stat="year_min"]')
ymax = soup.select('td[data-stat="year_max"]')

for html_tag in ymin:
    year_min.append(html_tag.string)
for html_tag in ymax:
    year_max.append(html_tag.string)

coach_list = pd.DataFrame({'Coach':coach_names,'Link':coach_url_list,'From':year_min, 'To':year_max, 'Birth Date':coach_birth_date, 'College':coach_college})

# number of coaches check
number_of_coaches = int(soup.find('h2').string.split(" ")[0])
if number_of_coaches == len(coach_url_list) and number_of_coaches == len(coach_names) and number_of_coaches == len(year_min) and number_of_coaches == len(year_max) and number_of_coaches == len(coach_birth_date) and number_of_coaches == len(coach_college):
    print("Same number",len(coach_url_list))
    coach_list.to_csv("coach_summary.csv")
else:
	print("Differing length, check again")