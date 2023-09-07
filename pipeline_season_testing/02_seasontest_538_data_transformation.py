#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 22:27:16 2023

@author: ian
"""

# Import packages

import pandas as pd 
import numpy as np 
import os
from pipeline_helper_functions import fix_team_names_fte, get_abbreviated_qb

import warnings
from pandas.errors import SettingWithCopyWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

current_season = 2023

five_thirty_eight = pd.read_csv('https://projects.fivethirtyeight.com/nfl-api/nfl_elo.csv')

# Only need recent data, and only need certain columns

fte = five_thirty_eight.copy()
fte = fte[fte.season >= current_season-1]
fte = fte[['date', 'season', 'neutral', 'playoff', 'team1', 'team2', 'qb1', 'qb2', 'score1', 'score2',
          'qb1_value_pre', 'qb2_value_pre', 'qbelo_prob1', 'qbelo_prob2']]

fte = fte.rename(columns = {
    'team1': 'home',
    'team2': 'away',
    'score1': 'home_score',
    'score2': 'away_score',
    'qb1': 'home_qb',
    'qb2': 'away_qb'
})

# Fix team names
    
fte['home'] = fte.apply(lambda x: fix_team_names_fte(x, home=True), axis=1)
fte['away'] = fte.apply(lambda x: fix_team_names_fte(x, home=False), axis=1)

# Remove games that have not occured yet

fte = fte[fte.home_score.notnull()]

# Save data frame

fte.to_csv('data/02_seasontest_538_data_transformation_results.csv')

# Get data frame with starting qb info

starting_qbs = fte[['date', 'season', 'home', 'away', 'home_score', 'away_score', 'home_qb', 'away_qb']]


starting_qbs['home_qb_abv'] = starting_qbs.apply(lambda x: get_abbreviated_qb(x.home_qb), axis=1)
starting_qbs['away_qb_abv'] = starting_qbs.apply(lambda x: get_abbreviated_qb(x.away_qb), axis=1)

starting_qbs.to_csv('data/02_seasontest_538_starting_qbs_list.csv')

print('02_538_data_transformation Complete')