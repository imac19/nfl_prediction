#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 22:08:50 2023

@author: ian
"""

# Fix team names

def fix_team_names(game, home=True):
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
    
    if home:
        return team_mapping[game['home_team']]
    
    else:
        return team_mapping[game['away_team']]
    
def fix_team_names_fte(game, home=True):
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
    
    if home:
        return team_mapping[game['home']]
    
    else:
        return team_mapping[game['away']]
    
def get_abbreviated_qb(qb):
    qb_split = qb.split('.')
    first = qb_split[0][0] + '.'
    last = qb_split[-1]
    qb_full = first + ' ' + last
    return qb_full