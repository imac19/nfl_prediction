# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 23:06:32 2023

@author: imacd_0odruq3
"""

# Import packages

import pandas as pd 
import numpy as np 
import os

# Import data

rb = pd.read_csv('data/04_seasontest_initial_rushing_values.csv')
rb = rb.drop(columns = ['Unnamed: 0'])
pass_def = pd.read_csv('data/04_seasontest_initial_pass_defense_values.csv')
pass_def = pass_def.drop(columns = ['Unnamed: 0'])
rush_def = pd.read_csv('data/04_seasontest_initial_rush_defense_values.csv')
rush_def = rush_def.drop(columns = ['Unnamed: 0'])
qb = pd.read_csv('data/04_seasontest_initial_qb_values.csv')
qb = qb.drop(columns = ['Unnamed: 0'])
qb = qb.drop(columns = ['Unnamed: 0.1'])
st = pd.read_csv('data/04_seasontest_initial_st_values.csv')
st = st.drop(columns = ['Unnamed: 0'])
extra = pd.read_csv('data/04_seasontest_initial_extra_values.csv')
extra = extra.drop(columns = ['Unnamed: 0'])

# Put data into one data frame that just has the game identifiers and value numbers

# qb = qb.copy()[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'qb', 'qb_value', 'passing_value']]
qb = qb.copy()[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'qb', 'passing_value']]
rb = rb.copy()[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'rushing_value']]
pass_def = pass_def.copy()[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'pass_def_value']]
rush_def = rush_def.copy()[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'rush_def_value']]
st = st.copy()[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'special_teams_value']]
extra = extra.copy()[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'total_plays_standardized', 'total_possession_time_standardized', 'pass_percentage_standardized']]
df = qb.copy()
df = df.merge(rb).merge(pass_def).merge(rush_def).merge(st).merge(extra)
df = df.drop_duplicates()

# Fix team names

# Move to helper functions

def fix_team_names(game, is_team=True):
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
    
    if is_team:
        return team_mapping[game['team']]
    
    else:
        return team_mapping[game['opponent']]
    
df['team_full'] = df.apply(lambda x: fix_team_names(x, is_team=True), axis=1)
df['opponent_full'] = df.apply(lambda x: fix_team_names(x, is_team=False), axis=1)

# Save raw data frame with values

df.to_csv('data/05_seasontest_value_models_combined.csv')

# Save data frame with past 5 games rolling stats

# Weighted average approach

def weighted_avg(values):
    if len(values) == 1:
        weights = np.array([1])
    elif len(values) == 2:
        weights = np.array([.25, .75])
    elif len(values) == 3:
        weights = np.array([.1, .3, .6])
    elif len(values) == 4:
        weights = np.array([.1, .15, .25, .5])
    elif len(values) == 5:
        weights = np.array([.1, .1, .15, .15, .5])
    
    return np.sum(weights * values)

# Uncomment and use this if even weights are desired

def weighted_avg(values):
    if len(values) == 1:
        weights = np.array([1])
    elif len(values) == 2:
        weights = np.array([.5, .5])
    elif len(values) == 3:
        weights = np.array([.333, .333, .333])
    elif len(values) == 4:
        weights = np.array([.25, .25, .25, .25])
    elif len(values) == 5:
        weights = np.array([.2, .2, .2, .2, .5])
    
    return np.sum(weights * values)

offense_base = df.copy()[['season', 'week', 'team', 'qb']]
defense_base = df.copy()[['season', 'week', 'team']]

offense_rolling = df[['team', 'qb', 'passing_value', 'rushing_value',
                     'total_plays_standardized', 'total_possession_time_standardized', 
                     'pass_percentage_standardized']]
offense_rolling = offense_rolling.groupby(by=['team', 'qb']).rolling(
    5, closed='left', min_periods=1).apply(lambda x: weighted_avg(x)).reset_index(level=['team', 'qb'], drop=True)

defense_rolling = df[['team', 'pass_def_value', 'rush_def_value', 'special_teams_value']]
defense_rolling = defense_rolling.groupby(by=['team']).rolling(
    5, closed='left', min_periods=1).apply(lambda x: weighted_avg(x)).reset_index(level=['team'], drop=True)

offense = offense_base.join(offense_rolling)
defense = defense_base.join(defense_rolling).dropna()

combined = offense.merge(defense, how='left')

# fix team names

combined['team_full'] = combined.apply(lambda x: fix_team_names(x, is_team=True), axis=1)

# Save aggregated data frame with values

combined.to_csv('data/05_seasontest_value_models_aggregated.csv')

print('05_value_models_combination_and_aggregation Complete')