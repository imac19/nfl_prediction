# def get_features(df):
#     return df[['total_pass_attempts', 'total_passing_yards', 'completions', 'passing_epa', 'pass_tds', 
#               'avg_cpoe', 'qb_rush_yards', 'qb_rushing_epa', 'qb_rush_tds', 'fumbles_qb', 'lost_fumbles_qb', 'interceptions_thrown_qb']]

def get_features(df):
    return df[['passing_epa_per_attempt']]

def get_label(df):
    return df[['qb_win']]