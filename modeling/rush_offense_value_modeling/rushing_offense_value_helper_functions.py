# def get_features(df):
#     return df[['total_rushes', 'total_rush_yards', 'rushing_epa', 'rush_tds']]

def get_features(df):
    return df[['rushing_epa_per_carry']]

def get_label(df):
    return df[['rb_win']]