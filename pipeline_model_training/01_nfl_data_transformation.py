#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:57:48 2023

@author: ian
"""

# Import packages

import pandas as pd 
import numpy as np 
import os
import nfl_data_py as nfl
import datetime
from pipeline_helper_functions import fix_team_names, get_abbreviated_qb

import warnings
from pandas.errors import SettingWithCopyWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

# Use nfl_data_py package to get data

nfl_df = nfl.import_pbp_data([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])

# Add column detailing if there was a qb designed run

rosters = nfl.import_rosters([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])
qb_roster = rosters[rosters.position == 'QB']
qb_roster = qb_roster[['position', 'player_name', 'player_id']].drop_duplicates()
qb_roster['player_id_string'] = qb_roster.apply(lambda x: str(x.player_id), axis=1)

def is_designed_qb_run(play, qb_roster):
    if play.rusher_id:
        if qb_roster.player_id_string.str.contains(str(play.rusher_id)).any():
            return 1 
    else: 
        return 0 
    
nfl_df['qb_designed_run'] = nfl_df.apply(lambda x: is_designed_qb_run(x, qb_roster), axis=1)

# Get important offensive NFL stats per game per team

# Get only offensive plays, take out qb kneels

offense = nfl_df[nfl_df.play_type.isin(['run', 'pass'])]
offense = offense[offense.qb_kneel == 0]

rushes = offense[offense.play_type == 'run']
rushing_grouped = rushes.groupby(by=['season', 'week', 'posteam'])
rush_df = rushing_grouped.count()['play_id'].rename('total_rushes').to_frame()
rush_df[['total_rush_yards', 'rushing_epa', 'rush_tds']] = rushing_grouped.sum()[['yards_gained', 'epa', 'rush_touchdown']]

print('Rushing Stats Complete')

# Get passing stats

# Total pass attempts, total pass yards, passing epa

passing_columns = ['season', 'week', 'posteam', 'passer_player_name', 'play_id', 'yards_gained',
                   'complete_pass', 'epa', 'pass_touchdown', 'air_yards', 'yards_after_catch', 
                   'air_epa', 'yac_epa', 'cpoe', 'sack']

passing = offense[offense.play_type == 'pass']
passing = passing[passing_columns]
passing_grouped = passing.groupby(by=['season', 'week', 'posteam', 'passer_player_name'])
passing_grouped_no_sacks = passing[passing.sack == 0].groupby(by=['season', 'week', 'posteam', 'passer_player_name'])
pass_df = passing_grouped_no_sacks.count()['play_id'].rename('total_pass_attempts').to_frame()
pass_df['total_passing_yards'] = passing_grouped_no_sacks.sum()['yards_gained']
passing_grouped_completions = passing[passing.complete_pass == 1].groupby(by=['season', 'week', 'posteam', 'passer_player_name'])
pass_df[['completions', 'passing_epa', 'pass_tds']] = passing_grouped.sum()[['complete_pass', 'epa', 'pass_touchdown']]
pass_df[['air_yards', 'yards_after_catch', 'air_epa', 'yac_epa']] = passing_grouped_completions.sum()[['air_yards', 'yards_after_catch', 'air_epa', 'yac_epa']]
pass_df['avg_cpoe'] = passing_grouped_no_sacks.mean()['cpoe'].rename('avg_cpoe').to_frame()
pass_df = pass_df.reset_index(level='passer_player_name').rename(columns = {'passer_player_name':'qb'})

print('Passing Stats Complete')

# Get other offensive stats

# Get qb epa and rushing stats
qb_stats = offense[(offense.play_type == 'pass') | (offense.qb_scramble == 1) | (offense.qb_designed_run == 1)]
qb_stats['qb'] = qb_stats.apply(lambda x: x.passer_player_name if x.passer_player_name is not None else x.rusher_player_name, axis=1)

qb_epa_df = qb_stats.groupby(by = ['season', 'week', 'posteam', 'qb']).sum()['qb_epa'].rename('qb_epa').to_frame()

qb_runs = offense[((offense.qb_scramble == 1) & (offense.pass_length.isnull())) | (offense.qb_designed_run == 1)]
qb_runs['qb'] = qb_runs.apply(lambda x: x.passer_player_name if x.passer_player_name is not None else x.rusher_player_name, axis=1)

qb_rush_grouped = qb_runs.groupby(by=['season', 'week', 'posteam', 'qb'])
qb_rush_df = qb_rush_grouped.sum()[['yards_gained', 'epa', 'rush_touchdown']]
qb_rush_df.columns = ['qb_rush_yards', 'qb_rushing_epa', 'qb_rush_tds']

qb_carries = qb_rush_grouped.count()['epa'].rename('total_qb_rush_attempts')

qb_turnovers = qb_stats.groupby(by=['season', 'week', 'posteam', 'qb']).sum()[['sack', 'qb_hit', 'fumble', 'fumble_lost', 'interception']]
qb_turnovers.columns = ['sacks_taken_qb', 'qb_hits_taken_qb', 'fumbles_qb', 'lost_fumbles_qb', 'interceptions_thrown_qb']

qb_final = qb_epa_df.merge(qb_rush_df, left_index=True, right_index=True, how='left')
qb_final = qb_final.merge(qb_carries, left_index=True, right_index=True, how='left')
qb_final = qb_final.merge(qb_turnovers, left_index=True, right_index=True, how='left')
qb_final = qb_final.fillna(0)

print('QB Stats Complete')

# Get sacks, interceptions, fumbles, fumbles lost, turnovers

turnovers_df = offense.groupby(by = ['season', 'week', 'posteam']).sum()[['sack', 'qb_hit', 'fumble', 'fumble_lost', 'interception']]
turnovers_df.columns = ['sacks_allowed_team', 'qb_hits_allowed_team', 'fumbles_team', 'lost_fumbles_team', 'interceptions_thrown_team']
turnovers_df.head(5)

print('Turnover Stats Complete')

# Get important defensive NFL stats per game per team

# Get only defensive plays, take out qb kneels

defense = nfl_df[nfl_df.play_type.isin(['run', 'pass'])]
defense = defense[defense.qb_kneel == 0]
defense.head(5)

# Get rushing defense stats

# Total rushes, total rush yards, rushing epa

rushes_def = defense[defense.play_type == 'run']
rushing_grouped_def = rushes.groupby(by=['season', 'week', 'defteam'])
rush_df_def = rushing_grouped_def.count()['play_id'].rename('total_rushes_allowed').to_frame()
rush_df_def[['total_rush_yards_allowed', 'rushing_epa_allowed', 'rush_tds_allowed']] = rushing_grouped_def.sum()[['yards_gained', 'epa', 'rush_touchdown']]

print('Rush Defense Stats Complete')

# Get passing defense stats

# Total pass attempts, total pass yards, passing epa

passing_def = defense[defense.play_type == 'pass']
passing_grouped_def = passing_def.groupby(by=['season', 'week', 'defteam'])
passing_grouped_def_no_sacks = passing_def[passing_def.sack == 0].groupby(by=['season', 'week', 'defteam'])
pass_df_def = passing_grouped_def_no_sacks.count()['play_id'].rename('total_pass_attempts_allowed').to_frame()
pass_df_def['passing_yards_allowed'] = passing_grouped_def_no_sacks.sum()['yards_gained']
passing_grouped_completions_def = passing_def[passing_def.complete_pass == 1].groupby(by=['season', 'week', 'defteam'])
pass_df_def[['completions_allowed', 'passing_epa_allowed', 'pass_tds_allowed']] = passing_grouped_def.sum()[['complete_pass', 'epa', 'pass_touchdown']]
pass_df_def[['air_yards_allowed', 'yards_after_catch_allowed', 'air_epa_allowed', 'yac_epa_allowed']] = passing_grouped_completions_def.sum()[['air_yards', 'yards_after_catch', 'air_epa', 'yac_epa']]
pass_df_def['avg_cpoe_allowed'] = passing_grouped_def_no_sacks.mean()['cpoe'].rename('avg_cpoe').to_frame()

print('Pass Defense Stats Complete')

# Get other defensive stats

# Get defensive qb epa and rushing stats
qb_stats_def = defense[(defense.play_type == 'pass') | (defense.qb_scramble == 1) | (defense.qb_designed_run == 1)]
qb_epa_df_def = qb_stats_def.groupby(by = ['season', 'week', 'defteam']).sum()['qb_epa'].rename('qb_epa_allowed').to_frame()

qb_runs_def = defense[((defense.qb_scramble == 1) & (defense.pass_length.isnull())) | (defense.qb_designed_run == 1)]
qb_rush_grouped_def = qb_runs_def.groupby(by=['season', 'week', 'defteam'])
qb_rush_df_def = qb_rush_grouped_def.sum()[['yards_gained', 'epa', 'rush_touchdown']]
qb_rush_df_def.columns = ['qb_rush_yards_allowed', 'qb_rushing_epa_allowed', 'qb_rush_tds_allowed']

qb_final_def = qb_epa_df_def.merge(qb_rush_df_def, left_index=True, right_index=True, how='left')
qb_final_def = qb_final_def.fillna(0)

print('QB Defense Stats Complete')

# Get sacks, interceptions, fumbles, fumbles lost, turnovers

turnovers_df_def = defense.groupby(by = ['season', 'week', 'defteam']).sum()[['sack', 'qb_hit', 'fumble_forced', 'interception']]
turnovers_df_def.columns = ['sacks', 'qb_hits', 'fumbles_forced', 'interceptions']
fumble_recovery_df = defense[(defense.defteam == defense.fumble_recovery_1_team)].groupby(by = ['season', 'week', 'defteam']).sum()['fumble_forced'].rename('fumbles_recovered').to_frame()
turnovers_df_def = turnovers_df_def.join(fumble_recovery_df, how='left').fillna(0)

print('Defensive Turnover Stats Complete')

# Get special teams stats

specials = nfl_df[nfl_df.special == 1]
specials_grouped = specials.groupby(by = ['season', 'week', 'posteam'])
specials_epa_df_one = specials_grouped.sum()['epa'].rename('special_teams_epa_one').to_frame()

specials = nfl_df[nfl_df.special == 1]
specials_grouped = specials.groupby(by = ['season', 'week', 'defteam'])
specials_epa_df_two = specials_grouped.sum()['epa'].rename('special_teams_epa_two').to_frame()

specials_epa_df = specials_epa_df_one.merge(specials_epa_df_two, left_on=['season', 'week', 'posteam'], right_index=True)
specials_epa_df['special_teams_epa'] = specials_epa_df.special_teams_epa_one - specials_epa_df.special_teams_epa_two
specials_epa_df.drop(columns = ['special_teams_epa_one', 'special_teams_epa_two'], inplace=True)

print('Special Teams Stats Complete')

# Get pass percentage, run percentage, etc. 

other_stats_offense = offense.copy()[['season', 'week', 'posteam', 'play_type', 'yards_gained']]
other_stats_offense = other_stats_offense.groupby(by=['season', 'week', 'posteam', 'play_type']).count().reset_index().rename(
columns = {'yards_gained':'total_plays'})
other_stats_offense = other_stats_offense.pivot(index = ['season', 'week', 'posteam'], columns = ['play_type'], values = ['total_plays'])
other_stats_offense = other_stats_offense.droplevel(None, axis=1).reset_index()
other_stats_offense['total_offensive_plays'] = other_stats_offense.apply(lambda x: x['pass'] + x.run, axis=1)
other_stats_offense['pass_percentage'] = other_stats_offense.apply(lambda x: x['pass']/x.total_offensive_plays, axis=1)
other_stats_offense['run_percentage'] = other_stats_offense.apply(lambda x: x.run/x.total_offensive_plays, axis=1)
other_stats_offense_df = other_stats_offense[['season', 'week', 'posteam', 'pass_percentage', 'run_percentage']]
other_stats_offense_df = other_stats_offense_df.rename(columns={'posteam':'team'})
other_stats_offense_df = other_stats_offense_df.rename_axis(None, axis=1)

print('Other Offensive Stats Complete')

# Get pace of play

drive_pace_and_results = nfl_df[nfl_df.play_type.notna()][['season', 'week', 'posteam', 'defteam', 'fixed_drive', 
                                                           'fixed_drive_result', 'drive_play_count', 
                                                           'drive_time_of_possession']]
drive_pace_join  = drive_pace_and_results.groupby(
    by=['season', 'week', 'posteam', 'defteam', 'fixed_drive'])['drive_play_count'].max().reset_index()
drive_pace_and_results = drive_pace_and_results.merge(
    drive_pace_join, on = ['season', 'week', 'posteam', 'defteam', 'fixed_drive', 'drive_play_count'],
    how = 'inner').drop_duplicates().dropna()
drive_pace_and_results['drive_time_of_possession'] = (pd.to_datetime(drive_pace_and_results['drive_time_of_possession'], 
                                                                    format='%M:%S') - datetime.datetime(1900, 1, 1)).dt.total_seconds()

drive_pace = drive_pace_and_results[['season', 'week', 'posteam', 'defteam', 'drive_play_count', 
                                     'drive_time_of_possession']].groupby(
    by=['season', 'week', 'posteam', 'defteam']).sum()
drive_pace = drive_pace.reset_index().rename(columns = {'drive_play_count':'total_plays',
                            'drive_time_of_possession':'total_possession_time_seconds',
                                         'posteam':'team'})
drive_pace = drive_pace[['season', 'week', 'team', 'total_plays', 'total_possession_time_seconds']]

print('Drive Pace Stats Complete')

# Get overall score and other game total stats

home_scores_and_etc_df = nfl_df.groupby(by = ['season', 'week', 'home_team', 'away_team']).max()[['home_score', 'away_score']]
home_scores_and_etc_df.index.names = ['season', 'week', 'team', 'opponent']
home_scores_and_etc_df.columns = ['score', 'opponent_score']
away_scores_and_etc_df = nfl_df.groupby(by = ['season', 'week', 'away_team', 'home_team']).max()[['away_score', 'home_score']]
away_scores_and_etc_df.index.names = ['season', 'week', 'team', 'opponent']
away_scores_and_etc_df.columns = ['score', 'opponent_score']

final_nfl_df = pd.concat([home_scores_and_etc_df, away_scores_and_etc_df])
final_nfl_df = final_nfl_df.sort_index().reset_index()

# Combine all stats together into one data frame

final_nfl_df = final_nfl_df.merge(
    pass_df, left_on=['season', 'week', 'team'], right_index=True).merge(
    rush_df, left_on=['season', 'week', 'team'], right_index=True).merge(
    qb_final, left_on=['season', 'week', 'team', 'qb'], right_index=True).merge(
    turnovers_df, left_on=['season', 'week', 'team'], right_index=True).merge(
    rush_df_def, left_on=['season', 'week', 'team'], right_index=True).merge(
    pass_df_def, left_on=['season', 'week', 'team'], right_index=True).merge(
    qb_final_def, left_on=['season', 'week', 'team'], right_index=True).merge(
    turnovers_df_def, left_on=['season', 'week', 'team'], right_index=True).merge(
    specials_epa_df, left_on=['season', 'week', 'team'], right_index=True).merge(
    drive_pace, left_on = ['season', 'week', 'team'], right_on = ['season', 'week', 'team']).merge(
    other_stats_offense_df, left_on = ['season', 'week', 'team'], right_on = ['season', 'week', 'team'])
        
print('Final Data Frame Complete')
        
# Flip sign of def epa 

# Add total epa stats

final_nfl_df['total_epa'] = final_nfl_df.apply(lambda x: x.passing_epa + x.rushing_epa + x.special_teams_epa - x.rushing_epa_allowed - x.passing_epa_allowed, axis = 1)
final_nfl_df['total_opposing_epa'] = -final_nfl_df.total_epa

# Fix QB Names

final_nfl_df_fixed_qb = final_nfl_df.copy()
final_nfl_df_fixed_qb['qb'] = final_nfl_df_fixed_qb.apply(lambda x: get_abbreviated_qb(x.qb), axis=1)

final_nfl_df_fixed_qb.to_csv('data/01_nfl_data_transformation_results.csv')

# Get game schedule and results

schedule_df = nfl_df.copy()
schedule_df = schedule_df[['season', 'week', 'home_team', 'away_team', 'home_score', 'away_score', 'season_type']].drop_duplicates()
schedule_df.head()
    
schedule_df['home_full'] = schedule_df.apply(lambda x: fix_team_names(x, home=True), axis=1)
schedule_df['away_full'] = schedule_df.apply(lambda x: fix_team_names(x, home=False), axis=1)
schedule_df.head()

schedule_df.to_csv('data/schedule_df.csv')

print('01_nfl_data_transformation Complete')