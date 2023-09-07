#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 23:52:02 2023

@author: ian
"""

# Import packages

import pandas as pd 
import numpy as np 
import os

import warnings
from pandas.errors import SettingWithCopyWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

nfl = pd.read_csv('data/01_nfl_data_transformation_results.csv')

nfl_sub = nfl[['season', 'week', 'team', 'opponent', 'qb', 'total_pass_attempts']]
nfl_sub['qb_ranking'] = nfl_sub.groupby(
    by=['season', 'week', 'team', 'opponent'])['total_pass_attempts'].rank(method='first', ascending=False)

lookup = nfl_sub[nfl_sub.qb_ranking==1]
lookup = lookup[['season', 'week', 'team', 'opponent', 'qb']]

lookup.to_csv('data/03_team_primary_qb_lookup_table.csv')

print('03_team_primary_qb_lookup Complete')
