import os
import csv
import sys
import pandas as pd

#CHANGE TO PATH WITH ALL NBA COACH INDIVIDUAL DATA
path = 'C:\\Users\\fan_t\\Desktop\\ICON\\BACT\\SportsAnalytics\\Deliverables\\nba_coach_individual\\'

#create empty dataframe with all required columns
all_col = ['name','season', 'age', 'lg_id', 'team_id', 'g', 'wins', 'losses', 'win_loss_pct', 'wins_over_500', 'rank_team', 'g_playoffs', 'losses_playoffs', 'win_loss_pct_playoffs', 'coach_remarks', 'role','League','Award'
,'Details']
full_panel = pd.DataFrame(columns=all_col)


os.chdir(path)
coach_list = os.listdir(path)
all_col = ['name','season', 'age', 'lg_id', 'team_id', 'g', 'wins', 'losses', 'win_loss_pct', 'wins_over_500', 'rank_team', 'g_playoffs', 'losses_playoffs', 'win_loss_pct_playoffs', 'coach_remarks', 'role','League','Award'
]
df_list = []
for coach in coach_list:
    partial_panel = pd.DataFrame(columns=all_col)
    os.chdir(path+coach)
    detail = os.listdir(path+coach)
    #print(detail)
    name = ' '.join(coach.split('_'))
    data = pd.read_csv(coach + '_Record.csv')
    data['name'] = name
    partial_panel = pd.concat([partial_panel, data],sort=False)
    try:
        award = pd.read_csv(coach+'_Award.csv')
        award.rename(columns={'Season': 'season'}, inplace=True)
        partial_panel_season = partial_panel.set_index('season')
        award_season = award.set_index('season')
        res = partial_panel_season.reindex(columns=partial_panel_season.columns.union(award_season.columns)) 
        res.update(award_season)
        res.reset_index(inplace=True)
        partial_panel = res
    except:
        pass
    df_list.append(partial_panel)
os.chdir(path)

# Data
print(len(df_list))
merged = pd.concat(df_list, axis=0)
print(merged.columns.values)
merged.to_csv('coach_panel_without_transaction.csv',index=False)
    
