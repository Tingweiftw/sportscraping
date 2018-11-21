import os
import csv
import sys
import pandas as pd


'''
1. CHANGE PATH TO SCRAPPED NFL INDIVIDUAL GAMELOG 'nfl_player_gamelog_url'
2. CREATE _partial_merge folder inside 
'''

path = 'C:\\Users\\fan_t\\Desktop\\ICON\\BACT\\SportsAnalytics\\Deliverables\\nfl_player_gamelog_url\\'

#Run this once to get full set of unique column for different NFL roles
'''
os.chdir(path)
list_of_alphabet = os.listdir(path)
set_of_columns = []
for letter in list_of_alphabet:
    os.chdir(path+letter)
    file_in_directory = os.listdir()
    for file in file_in_directory:
        data = pd.read_csv(file)
        #print(list(data.columns.values))
        set_of_columns += list(data.columns.values)
        set_of_columns = list(set(set_of_columns))
for i in common_col:
    if i in set_of_columns:
        set_of_columns.remove(i)
set_of_columns
'''
os.chdir(path)
list_of_alphabet = os.listdir(path)
common_col = ['Year', 'Date', 'G#', 'Age', 'Tm', 'Unnamed: 5', 'Opp', 'Result', 'GS']
set_of_columns=['Scoring.FGA',
 'Receiving.Yds',
 'Punting.Y/P',
 'Def Interceptions.Int',
 'Passing.AY/A',
 'Scoring.Pts',
 'Punting.Yds',
 'Rushing.Y/A',
 'Passing.Att',
 'Receiving.Y/R',
 'Receiving.Ctch%',
 'Tackles.TFL',
 'Kick Returns.Rt',
 'Tackles.QBHits',
 'Kick Returns.Y/Rt',
 'Passing.TD',
 'Passing.Y/A',
 'Receiving.Tgt',
 'Punting.Blck',
 'Punt Returns.TD',
 'Tackles.Comb',
 'Sk',
 'Punting.Pnt',
 'Punt Returns.Ret',
 'Passing.Yds.1',
 'Scoring.XPM',
 'Scoring.FG%',
 'Scoring.XP%',
 'Def Interceptions.PD',
 'Scoring.Sfty',
 'Tackles.Ast',
 'Def Interceptions.Yds',
 'Punt Returns.Y/R',
 'Def Interceptions.TD',
 'Scoring.XPA',
 'Kick Returns.TD',
 'Passing.Rate',
 'Tackles.Solo',
 'Rushing.TD',
 'Passing.Sk',
 'Receiving.Rec',
 'Scoring.TD',
 'Passing.Yds',
 'Rushing.Yds',
 'Passing.Cmp%',
 'Punt Returns.Yds',
 'Passing.Int',
 'Scoring.FGM',
 'Passing.Cmp',
 'Kick Returns.Yds',
 'Receiving.TD',
 'Receiving.Y/Tgt',
 'Scoring.2PM',
 'Rushing.Att']
all_col = common_col + sorted(set_of_columns)
all_col.insert(0,'Name')
all_col.insert(0,'ID')

#Merge for each alphabet
for letter in list_of_alphabet:
    full_panel = pd.DataFrame(columns=all_col)
    os.chdir(path+letter)
    file_in_directory = os.listdir()
    print(len(file_in_directory))
    print('Starting with',letter)
    count = 0
    for file in file_in_directory:
        identity = file.split('^')
        data = pd.read_csv(file)
        data['Name'] = identity[1].split('.')[0]
        data['ID'] = identity[0]
        full_panel = pd.concat([full_panel, data],sort=False)
        count+=1
    print(count)
    print(list(os.listdir()))
    os.chdir(path + '_partial_merge')
    full_panel.to_csv(letter+'.csv', encoding='utf-8', index=False)
    print('Done with',letter)

#Final merge with all alphabet
os.chdir(Path+'_partial_merge')
list_of_file = os.listdir(path+'_partial_merge')
df_list = []
for file in list_of_file:
    f = pd.read_csv(file,low_memory=False)
    df_list.append(f)
    print('append',file)
merged = pd.concat(df_list, axis=0)
merged.to_csv('merged1.csv',index=False)
print('done')