import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np

# Historical Head-to-Head win percentage matrix between IPL teams
H2H_WIN_MATRIX = {
    ('Chennai Super Kings', 'Mumbai Indians'): 0.45,
    ('Mumbai Indians', 'Chennai Super Kings'): 0.55,
    ('Chennai Super Kings', 'Royal Challengers Bengaluru'): 0.65,
    ('Royal Challengers Bengaluru', 'Chennai Super Kings'): 0.35,
    ('Mumbai Indians', 'Royal Challengers Bengaluru'): 0.60,
    ('Royal Challengers Bengaluru', 'Mumbai Indians'): 0.40,
    ('Kolkata Knight Riders', 'Royal Challengers Bengaluru'): 0.55,
    ('Royal Challengers Bengaluru', 'Kolkata Knight Riders'): 0.45,
    ('Gujarat Titans', 'Rajasthan Royals'): 0.60,
    ('Rajasthan Royals', 'Gujarat Titans'): 0.40,
}

def get_h2h_win_pct(batting_team, bowling_team):
    """Returns historical win percentage of batting_team vs bowling_team."""
    key = (batting_team, bowling_team)
    if key in H2H_WIN_MATRIX:
        return H2H_WIN_MATRIX[key]
    return 0.50  # Default balanced 50% H2H


def compute_derived_features(df):
    """
    Computes all match situation metrics from ball-by-ball 2nd innings data.
    """
    df = df.copy()

    # Overs completed float (e.g., 5 overs and 3 balls = 5.5 overs)
    if 'overs_completed' not in df.columns:
        df['overs_completed'] = df['over'] + (df['ball'] / 6.0)

    # Balls remaining in 20-over match
    if 'balls_left' not in df.columns:
        df['balls_left'] = np.maximum(0, 120 - (df['over'] * 6 + df['ball']))

    # Wickets in hand
    df['wickets_remaining'] = np.maximum(0, 10 - df['wickets_fallen'])

    # Runs remaining
    df['runs_left'] = np.maximum(0, df['target_runs'] - df['current_score'])

    # Current Run Rate (CRR)
    df['crr'] = np.where(
        df['overs_completed'] > 0,
        df['current_score'] / df['overs_completed'],
        0.0
    )

    # Required Run Rate (RRR)
    df['rrr'] = np.where(
        df['balls_left'] > 0,
        (df['runs_left'] * 6.0) / df['balls_left'],
        np.where(df['runs_left'] == 0, 0.0, 99.0)
    )

    # Match Phase
    def assign_phase(over):
        if over < 6:
            return 'Powerplay'
        elif over < 15:
            return 'Middle'
        else:
            return 'Death'

    df['phase'] = df['over'].apply(assign_phase)

    # Head-to-Head Win Rate Feature
    if 'batting_team' in df.columns and 'bowling_team' in df.columns:
        df['h2h_win_pct'] = df.apply(
            lambda row: get_h2h_win_pct(row['batting_team'], row['bowling_team']), axis=1
        )
    else:
        df['h2h_win_pct'] = 0.50

    # Toss Flag
    if 'toss_winner' in df.columns and 'batting_team' in df.columns:
        df['toss_winner_is_batting'] = (df['toss_winner'] == df['batting_team']).astype(int)
    else:
        df['toss_winner_is_batting'] = 0

    return df


def prepare_feature_matrix(df):
    """
    Selects feature columns X and target variable y.
    Returns (X, y, categorical_cols, numerical_cols).
    """
    df_feat = compute_derived_features(df)

    categorical_cols = ['batting_team', 'bowling_team', 'venue', 'phase']
    numerical_cols = [
        'current_score',
        'wickets_fallen',
        'wickets_remaining',
        'overs_completed',
        'balls_left',
        'target_runs',
        'runs_left',
        'crr',
        'rrr',
        'h2h_win_pct',
        'toss_winner_is_batting'
    ]

    feature_cols = categorical_cols + numerical_cols
    X = df_feat[feature_cols]
    
    # Target
    if 'is_chaser_winner' in df_feat.columns:
        y = df_feat['is_chaser_winner'].values
    else:
        y = (df_feat['winner'] == df_feat['batting_team']).astype(int).values

    groups = df_feat['match_id'].values if 'match_id' in df_feat.columns else None

    return X, y, groups, categorical_cols, numerical_cols

