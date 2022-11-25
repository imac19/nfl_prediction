def get_features(df):
    return df[['epa_allowed_per_carry']]

def get_label(df):
    return df[['rush_def_win']]