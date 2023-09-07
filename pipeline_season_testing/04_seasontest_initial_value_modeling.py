#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 13:00:47 2023

@author: ian
"""

# Import packages

import pandas as pd 
import numpy as np 
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import statsmodels.api as sm
from scipy import stats

from joblib import dump, load

nfl = pd.read_csv('data/01_seasontest_nfl_data_transformation_results.csv')
qb_lookup = pd.read_csv('data/03_seasontest_team_primary_qb_lookup_table.csv')

# Take only the passing/qb stats

passing = nfl.copy()
passing = passing[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'qb', 'total_pass_attempts', 'total_passing_yards',
        'completions', 'passing_epa', 'pass_tds', 'air_yards', 'yards_after_catch', 'air_epa', 'yac_epa', 'avg_cpoe',
        'qb_epa', 'total_qb_rush_attempts', 'qb_rush_yards', 'qb_rushing_epa', 'qb_rush_tds', 'sacks_taken_qb', 'qb_hits_taken_qb', 'fumbles_qb',
        'lost_fumbles_qb', 'interceptions_thrown_qb']]
passing = passing[passing.total_pass_attempts > 10]
passing = passing.merge(qb_lookup)

qb_epa_mean = np.mean(passing.qb_epa)
qb_epa_std = np.std(passing.qb_epa)
passing['qb_epa_standardized'] = passing.apply(lambda x: (x.qb_epa - qb_epa_mean)/qb_epa_std, axis=1)
passing['qb_epa_per_attempt'] = passing.apply(lambda x: x.qb_epa/(x.total_pass_attempts + x.total_qb_rush_attempts), axis=1)

passing_epa_mean = np.mean(passing.passing_epa)
passing_epa_std = np.std(passing.passing_epa)
passing['passing_epa_standardized'] = passing.apply(lambda x: (x.passing_epa - passing_epa_mean)/passing_epa_std, axis=1)
passing['passing_epa_per_attempt'] = passing.apply(lambda x: x.passing_epa/(x.total_pass_attempts), axis=1)

passing_no_glennon = passing[passing.qb_epa_per_attempt >= -2.5]
qb_epa_pa_mean = np.mean(passing_no_glennon.qb_epa_per_attempt)
qb_epa_pa_std = np.std(passing_no_glennon.qb_epa_per_attempt)

passing_epa_pa_mean = np.mean(passing_no_glennon.passing_epa_per_attempt)
passing_epa_pa_std = np.std(passing_no_glennon.passing_epa_per_attempt)

passing['qb_epa_per_attempt_standardized'] = passing.apply(lambda x: (x.qb_epa_per_attempt - qb_epa_pa_mean)/qb_epa_pa_std, axis=1)
passing['passing_epa_per_attempt_standardized'] = passing.apply(lambda x: (x.passing_epa_per_attempt - passing_epa_pa_mean)/passing_epa_pa_std, axis=1)

qb_to_save = passing.copy()
qb_to_save['qb_value'] = qb_to_save.qb_epa_per_attempt_standardized
qb_to_save['passing_value'] = qb_to_save.passing_epa_per_attempt_standardized

qb_to_save.to_csv('data/04_seasontest_initial_qb_values.csv')

# Pull out only the rushing related stats

rushing = nfl.copy()
rushing = rushing[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'total_rushes', 'total_rush_yards', 
       'rushing_epa', 'rush_tds', 'qb_rush_yards', 'qb_rushing_epa', 'qb_rush_tds']]
rushing = rushing.drop_duplicates()

# Pull out only the rushing related stats, minus the qb specific ones

rb = nfl.copy()
rb = rb[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'total_rushes', 'total_rush_yards', 
       'rushing_epa', 'rush_tds']]
rb = rb.drop_duplicates()

rushing_epa_mean = np.mean(rb.rushing_epa)
rushing_epa_std = np.std(rb.rushing_epa)
rb['rushing_epa_standardized'] = rb.apply(lambda x: (x.rushing_epa - rushing_epa_mean)/rushing_epa_std, axis=1)
rb['rushing_epa_per_attempt'] = rb.apply(lambda x: x.rushing_epa/x.total_rushes, axis=1)

rb_no_bears = rb[rb.rushing_epa_per_attempt > -1.5]
rushing_epa_pa_mean = np.mean(rb_no_bears.rushing_epa_per_attempt)
rushing_epa_pa_std = np.std(rb_no_bears.rushing_epa_per_attempt)
rb['rushing_epa_per_attempt_standardized'] = rb.apply(lambda x: (x.rushing_epa_per_attempt - rushing_epa_pa_mean)/rushing_epa_pa_std, axis=1)

rb_to_save = rb.copy()
rb_to_save['rushing_value'] = rb_to_save.rushing_epa_per_attempt_standardized

rb_to_save.to_csv('data/04_seasontest_initial_rushing_values.csv')

# Pull out only the pass defense related stats

pass_def = nfl.copy()
pass_def = pass_def[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'total_pass_attempts_allowed', 'passing_yards_allowed',
        'completions_allowed', 'passing_epa_allowed', 'pass_tds_allowed', 'air_yards_allowed', 'yards_after_catch_allowed', 'air_epa_allowed', 'yac_epa_allowed', 'avg_cpoe_allowed',
        'qb_epa_allowed', 'qb_rush_yards_allowed', 'qb_rushing_epa_allowed', 'qb_rush_tds_allowed', 'sacks', 'qb_hits', 'fumbles_forced',
        'fumbles_recovered', 'interceptions']]
pass_def = pass_def.drop_duplicates()

passing_epa_allowed_mean = np.mean(pass_def.passing_epa_allowed)
passing_epa_allowed_std = np.std(pass_def.passing_epa_allowed)
pass_def['passing_epa_allowed_standardized'] = pass_def.apply(lambda x: (x.passing_epa_allowed - passing_epa_allowed_mean)/passing_epa_allowed_std, axis=1)

pass_def['passing_epa_per_attempt_allowed'] = pass_def.apply(lambda x: x.passing_epa_allowed/x.total_pass_attempts_allowed, axis=1)
passing_no_glennon = pass_def[pass_def.passing_epa_per_attempt_allowed >= -3]

passing_epa_paa_mean = np.mean(passing_no_glennon.passing_epa_per_attempt_allowed)
passing_epa_paa_std = np.std(passing_no_glennon.passing_epa_per_attempt_allowed)
pass_def['passing_epa_per_attempt_allowed_standardized'] = pass_def.apply(lambda x: (x.passing_epa_per_attempt_allowed - passing_epa_paa_mean)/passing_epa_paa_std, axis=1)

passing_def_to_save = pass_def.copy()
passing_def_to_save['pass_def_value'] = -passing_def_to_save.passing_epa_per_attempt_allowed_standardized

passing_def_to_save.to_csv('data/04_seasontest_initial_pass_defense_values.csv')

# Pull out only the rushing defense related stats

rush_def = nfl.copy()
rush_def = rush_def[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'total_rushes_allowed', 'total_rush_yards_allowed', 
       'rushing_epa_allowed', 'rush_tds_allowed']]
rush_def = rush_def.drop_duplicates()

rushing_epa_allowed_mean = np.mean(rush_def.rushing_epa_allowed)
rushing_epa_allowed_std = np.std(rush_def.rushing_epa_allowed)
rush_def['rushing_epa_allowed_standardized'] = rush_def.apply(lambda x: (x.rushing_epa_allowed - rushing_epa_allowed_mean)/rushing_epa_allowed_std, axis=1)

rush_def['rushing_epa_per_attempt_allowed'] = rush_def.apply(lambda x: x.rushing_epa_allowed/x.total_rushes_allowed, axis=1)
rush_def_no_bears = rush_def[rush_def.rushing_epa_per_attempt_allowed > -1.5]

rushing_epa_paa_mean = np.mean(rush_def_no_bears.rushing_epa_per_attempt_allowed)
rushing_epa_paa_std = np.std(rush_def_no_bears.rushing_epa_per_attempt_allowed)
rush_def['rushing_epa_per_attempt_allowed_standardized'] = rush_def.apply(lambda x: (x.rushing_epa_per_attempt_allowed - rushing_epa_paa_mean)/rushing_epa_paa_std, axis=1)

rush_def_to_save = rush_def.copy()
rush_def_to_save['rush_def_value'] = -rush_def_to_save.rushing_epa_allowed_standardized

rush_def_to_save.to_csv('data/04_seasontest_initial_rush_defense_values.csv')

# Get special teams stats

st = nfl.copy()
st = st[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'special_teams_epa']]
st = st.drop_duplicates()

# Removing some outliers

st_no_outliers = st.copy()
st_no_outliers = st_no_outliers[np.abs(st_no_outliers.special_teams_epa) <= 15]

st_epa_mean = np.mean(st_no_outliers.special_teams_epa)
st_epa_std = np.std(st_no_outliers.special_teams_epa)
st['special_teams_epa_standardized'] = st.apply(lambda x: (x.special_teams_epa - st_epa_mean)/st_epa_std, axis=1)

st_to_save = st.copy()
st_to_save['special_teams_value'] = st_to_save.special_teams_epa_standardized

st_to_save.to_csv('data/04_seasontest_initial_st_values.csv')

# Get extra stats

extra = nfl.copy()
extra = extra[['season', 'week', 'team', 'opponent', 'score', 'opponent_score', 'total_plays', 'total_possession_time_seconds',
              'pass_percentage', 'run_percentage']]
extra = extra.drop_duplicates()
extra

# Removing some outliers

extra_no_outliers = extra.copy()
extra_no_outliers = extra_no_outliers[extra_no_outliers.run_percentage < .9]
extra_no_outliers

# Total plays

total_plays_mean = np.mean(extra_no_outliers.total_plays)
total_plays_std = np.std(extra_no_outliers.total_plays)
extra['total_plays_standardized'] = extra.apply(lambda x: (x.total_plays - total_plays_mean)/total_plays_std, axis=1)

# Total possession time

total_possession_time_mean = np.mean(extra_no_outliers.total_possession_time_seconds)
total_possession_time_std = np.std(extra_no_outliers.total_possession_time_seconds)
extra['total_possession_time_standardized'] = extra.apply(lambda x: (x.total_possession_time_seconds - total_possession_time_mean)/total_possession_time_std, axis=1)

# Pass percentage

pass_percentage_mean = np.mean(extra_no_outliers.pass_percentage)
pass_percentage_std = np.std(extra_no_outliers.pass_percentage)
extra['pass_percentage_standardized'] = extra.apply(lambda x: (x.pass_percentage - pass_percentage_mean)/pass_percentage_std, axis=1)

# Run percentage

# run_percentage_mean = np.mean(extra_no_outliers.run_percentage)
# run_percentage_std = np.std(extra_no_outliers.run_percentage)
# extra['run_percentage_standardized'] = extra.apply(lambda x: (x.run_percentage - run_percentage_mean)/run_percentage_std, axis=1)

extra_to_save = extra.copy()
extra_to_save.to_csv('data/04_seasontest_initial_extra_values.csv')

print('04_initial_value_modeling Complete')