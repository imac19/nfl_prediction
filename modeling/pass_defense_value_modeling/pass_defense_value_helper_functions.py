def get_features(df):
    return df[['passing_epa_per_attempt_allowed']]

def get_label(df):
    return df[['pass_def_win']]