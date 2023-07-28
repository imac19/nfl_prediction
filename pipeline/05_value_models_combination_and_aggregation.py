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

rb = pd.read_csv('data/initial_rushing_values.csv')
rb = rb.drop(columns = ['Unnamed: 0'])
pass_def = pd.read_csv('data/initial_pass_defense_values.csv')
pass_def = pass_def.drop(columns = ['Unnamed: 0'])
rush_def = pd.read_csv('data/initial_rush_defense_values.csv')
rush_def = rush_def.drop(columns = ['Unnamed: 0'])
qb = pd.read_csv('data/initial_qb_values.csv')
qb = qb.drop(columns = ['Unnamed: 0'])
st = pd.read_csv('data/initial_st_values.csv')
st = st.drop(columns = ['Unnamed: 0'])
extra = pd.read_csv('data/initial_extra_values.csv')
extra = extra.drop(columns = ['Unnamed: 0'])

