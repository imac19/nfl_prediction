#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 13:10:04 2023

@author: ian
"""

# Import packages

import pandas as pd 
import numpy as np 
import os

nfl = pd.read_csv('data/05_value_models_combined.csv')
nfl_rolling = pd.read_csv('data/05_value_models_aggregated.csv')

# Move to helper functions later

def value_adjustment(value, adjusting_value, original_value_percentage=.95, adjustment_threshold=.1):
    value_over_expected = value + adjusting_value
    adjusted_value = (value_over_expected*adjustment_threshold) + (value*original_value_percentage)
    adjustment = adjusted_value - value
    
    return adjustment, adjusted_value

qb = nfl[['season', 'week', 'team', 'opponent', 'team_full', 'opponent_full', 'score', 'opponent_score', 
          'qb', 'passing_value']]
opposing_def = nfl_rolling[['season', 'week', 'team_full', 
          'pass_def_value']]

df = qb.merge(opposing_def, left_on=['season', 'week', 'opponent_full'], 
             right_on=['season', 'week', 'team_full'], suffixes = ('','_opponent'))
df = df.drop(columns=['team_full_opponent'])

df[['pass_value_adjustment', 'passing_value_adjusted']] = df.apply(lambda x: value_adjustment(x.passing_value, x.pass_def_value, 
                                original_value_percentage=.8, adjustment_threshold=.2), axis=1, result_type='expand')

df.to_csv('data/06_adjusted_qb_values.csv')

rb = nfl[['season', 'week', 'team', 'opponent', 'team_full', 'opponent_full', 'score', 'opponent_score',
          'rushing_value']]
opposing_def = nfl_rolling[['season', 'week', 'team_full', 
          'rush_def_value']]

df = rb.merge(opposing_def, left_on=['season', 'week', 'opponent_full'], 
             right_on=['season', 'week', 'team_full'], suffixes = ('','_opponent'))
df = df.drop(columns=['team_full_opponent'])

df[['rushing_adjustment', 'rushing_value_adjusted']] = df.apply(lambda x: value_adjustment(x.rushing_value, x.rush_def_value, 
                                original_value_percentage=.8, adjustment_threshold=.2), axis=1, result_type='expand')

df.to_csv('data/06_adjusted_rushing_values.csv')

pass_def = nfl[['season', 'team', 'opponent', 'week', 'team_full', 'opponent_full', 'score', 'opponent_score',
          'pass_def_value']]
opposing_off = nfl_rolling[['season', 'week', 'team_full', 
          'passing_value']]

df = pass_def.merge(opposing_off, left_on=['season', 'week', 'opponent_full'], 
             right_on=['season', 'week', 'team_full'], suffixes = ('','_opponent'))
df = df.drop(columns=['team_full_opponent'])

df[['pass_def_adjustment', 'pass_def_value_adjusted']] = df.apply(lambda x: value_adjustment(x.pass_def_value, x.passing_value, 
                                original_value_percentage=.8, adjustment_threshold=.2), axis=1, result_type='expand')

df.to_csv('data/06_adjusted_pass_defense_values.csv')

rush_def = nfl[['season', 'team', 'opponent', 'week', 'team_full', 'opponent_full', 'score', 'opponent_score',
          'rush_def_value']]
opposing_off = nfl_rolling[['season', 'week', 'team_full', 
          'rushing_value']]

df = rush_def.merge(opposing_off, left_on=['season', 'week', 'opponent_full'], 
             right_on=['season', 'week', 'team_full'], suffixes = ('','_opponent'))
df = df.drop(columns=['team_full_opponent'])

df[['rush_def_adjustment', 'rush_def_value_adjusted']] = df.apply(lambda x: value_adjustment(x.rush_def_value, x.rushing_value, 
                                original_value_percentage=.8, adjustment_threshold=.2), axis=1, result_type='expand')

df.to_csv('data/06_adjusted_rush_defense_values.csv')

print('06_adjusted_value_modeling Complete')