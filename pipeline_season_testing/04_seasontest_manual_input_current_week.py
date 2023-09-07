#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 00:39:08 2023

@author: ian
"""

# Import packages

import pandas as pd 
import numpy as np 
import os

# Manual Input of current week games

# UPDATE THIS before each run

current_week = 1
current_season = 2023

qbs = pd.read_csv('data/03_seasontest_team_primary_qb_lookup_table.csv')

# Fix team names

# Move to helper functions

def fix_team_names(team_abrv):
    team_mapping = {
        'ARI':'Arizona Cardinals',
        'ATL':'Atlanta Falcons',
        'BAL':'Baltimore Ravens',
        'BUF':'Buffalo Bills',
        'CAR':'Carolina Panthers',
        'CHI':'Chicago Bears',
        'CIN':'Cincinnati Bengals',
        'CLE':'Cleveland Browns',
        'DAL':'Dallas Cowboys',
        'DEN':'Denver Broncos',
        'DET':'Detroit Lions',
        'GB':'Green Bay Packers',
        'HOU':'Houston Texans',
        'IND':'Indianapolis Colts',
        'JAX':'Jacksonville Jaguars',
        'KC':'Kansas City Chiefs',
        'OAK':'Las Vegas Raiders',
        'LV':'Las Vegas Raiders',
        'LAC':'Los Angeles Chargers',
        'LAR':'Los Angeles Rams',
        'LA':'Los Angeles Rams',
        'MIA':'Miami Dolphins',
        'MIN':'Minnesota Vikings',
        'NE':'New England Patriots',
        'NO':'New Orleans Saints',
        'NYG':'New York Giants',
        'NYJ':'New York Jets',
        'PHI':'Philadelphia Eagles',
        'PIT':'Pittsburgh Steelers',
        'SF':'San Francisco 49ers',
        'SEA':'Seattle Seahawks',
        'TB':'Tampa Bay Buccaneers',
        'TEN':'Tennessee Titans',
        'WSH':'Washington Football Team',
        'WAS':'Washington Football Team'
    }

    return team_mapping[team_abrv]

    
qbs['team_full'] = qbs.apply(lambda x: fix_team_names(x.team), axis=1)

if current_week == 1:
    check_week = 18
    check_season = current_season-1
    
else:
    check_week = current_week - 1
    check_season = current_season

current_week_qbs = qbs[(qbs.season == check_season) & (qbs.week == check_week)]
current_week_qbs = current_week_qbs[['season', 'week', 'team', 'team_full', 'qb']]
current_week_qbs['week'] = current_week
current_week_qbs['season'] = current_season

qb_dict = {game['team_full']:game['qb'] for index, game in current_week_qbs.iterrows()}

# QB Updates, if necessary

# qb_dict['Arizona Cardinals'] = 'Kyler Murray'
# qb_dict['Atlanta Falcons'] = 'Marcus Mariota'
# qb_dict['Baltimore Ravens'] = 'Lamar Jackson'
# qb_dict['Buffalo Bills'] = 'Josh Allen'
# qb_dict['Carolina Panthers'] = 'P.J. Walker'
# qb_dict['Chicago Bears'] = 'Trevor Siemian'
# qb_dict['Cincinnati Bengals'] = 'Joe Burrow'
# qb_dict['Cleveland Browns'] = 'Jacoby Brissett'
# qb_dict['Dallas Cowboys'] = 'Dak Prescott'
# qb_dict['Denver Broncos'] = 'Russell Wilson'
# qb_dict['Detroit Lions'] = 'Jared Goff'
# qb_dict['Green Bay Packers'] = 'Aaron Rodgers'
# qb_dict['Houston Texans'] = 'Kyle Allen'
# qb_dict['Indianapolis Colts'] = 'Matt Ryan'
# qb_dict['Jacksonville Jaguars'] = 'Trevor Lawrence'
# qb_dict['Kansas City Chiefs'] = 'Patrick Mahomes'
# qb_dict['Las Vegas Raiders'] = 'Derek Carr'
# qb_dict['Los Angeles Chargers'] = 'Justin Herbert'
# qb_dict['Los Angeles Rams'] = 'Matthew Stafford'
# qb_dict['Miami Dolphins'] = 'Tua Tagovailoa'
# qb_dict['Minnesota Vikings'] = 'Kirk Cousins'
# qb_dict['New England Patriots'] = 'Mac Jones'
# qb_dict['New Orleans Saints'] = 'Andy Dalton'
# qb_dict['New York Giants'] = 'Daniel Jones'
# qb_dict['New York Jets'] = 'Mike White'
# qb_dict['Philadelphia Eagles'] = 'Jalen Hurts'
# qb_dict['Pittsburgh Steelers'] = 'Kenny Pickett'
# qb_dict['San Francisco 49ers'] = 'Jimmy Garoppolo'
# qb_dict['Seattle Seahawks'] = 'Geno Smith'
# qb_dict['Tampa Bay Buccaneers'] = 'Tom Brady'
# qb_dict['Tennessee Titans'] = 'Ryan Tannehill'
# qb_dict['Washington Football Team'] = 'Taylor Heinicke'

# CHECK: Are qbs correct?

# IF NOT, update in previous step. Otherwise, good to go

for team, qb in qb_dict.items():
    print('{}: {}'.format(team, qb))
    print()

# Manually Inputted
# While not ideal, manually inputting the odds/games in doesn't take too much time/effort
# In the future, want to create a web scraping bot to automate getting the necessary odds and game data
# For now, this will have to do

# Column Order
# 'season', 'week', 'away', 'home', 'away_moneyline', 'home_moneyline', 'away_spread', 'over_under'

manual_input = {
    '{}{}{}'.format(current_season, current_week, 1): [current_season, current_week, 'DET','KC',
                                                      185, -225, 4.5, 52.5]
#     '{}{}{}'.format(current_season, current_week, 2): [current_season, current_week, 'NYG','DAL',
#                                                       350, -435, 10, -10, 45.5],
#     '{}{}{}'.format(current_season, current_week, 3): [current_season, current_week, 'NE','MIN',
#                                                       115, -135, 2.5, -2.5, 42.5],
#     '{}{}{}'.format(current_season, current_week, 4): [current_season, current_week, 'HOU','MIA',
#                                                       550, -750, 13.5, -13.5, 47],
#     '{}{}{}'.format(current_season, current_week, 5): [current_season, current_week, 'BAL','JAX',
#                                                       -195, 165, -3.5, 3.5, 43.5],
#     '{}{}{}'.format(current_season, current_week, 6): [current_season, current_week, 'CHI','NYJ',
#                                                       215, -255, 6, -6, 38.5],
#     '{}{}{}'.format(current_season, current_week, 7): [current_season, current_week, 'CIN','TEN',
#                                                       -150, 130, -2.5, 2.5, 42.5],
#     '{}{}{}'.format(current_season, current_week, 8): [current_season, current_week, 'ATL','WAS',
#                                                       170, -200, 4.5, -4.5, 40.5],
#     '{}{}{}'.format(current_season, current_week, 9): [current_season, current_week, 'DEN','CAR',
#                                                       -130, 110, -1.5, 1.5, 36],
#     '{}{}{}'.format(current_season, current_week, 10): [current_season, current_week, 'TB','CLE',
#                                                       -180, 155, -3.5, 3.5, 42],
#     '{}{}{}'.format(current_season, current_week, 11): [current_season, current_week, 'LV','SEA',
#                                                       165, -195, 3.5, -3.5, 48],
#     '{}{}{}'.format(current_season, current_week, 12): [current_season, current_week, 'LAC','ARI',
#                                                       -175, 150, -3, 3, 48],
#     '{}{}{}'.format(current_season, current_week, 13): [current_season, current_week, 'LAR','KC',
#                                                       750, -1150, 15.5, -15.5, 42],
#     '{}{}{}'.format(current_season, current_week, 14): [current_season, current_week, 'NO','SF',
#                                                       330, -410, 9.5, -9.5, 43.5],
#     '{}{}{}'.format(current_season, current_week, 15): [current_season, current_week, 'GB','PHI',
#                                                       245, -295, 6.5, -6.5, 43.5]
#     '{}{}{}'.format(current_season, current_week, 16): [current_season, current_week, 'LV','KC',
#                                                       265, -320, 7, -7, 51.5]
}


current_week_data = pd.DataFrame.from_dict(manual_input, orient='index',
                                          columns = ['season', 'week', 'away', 'home', 
                                                    'away_moneyline', 'home_moneyline', 
                                                    'away_spread', 'over_under'])
current_week_data['home_full_name'] = current_week_data.apply(lambda x: fix_team_names(x.home), axis=1)
current_week_data['away_full_name'] = current_week_data.apply(lambda x: fix_team_names(x.away), axis=1)
current_week_data['home_qb'] = current_week_data.apply(lambda x: qb_dict[x.home_full_name], axis=1)
current_week_data['away_qb'] = current_week_data.apply(lambda x: qb_dict[x.away_full_name], axis=1)

current_week_data.to_csv('data/04_seasontest_current_week_data.csv')
