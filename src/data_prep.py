import os
import urllib.request
import pandas as pd
import numpy as np

# Canonical IPL Teams list (handling renames e.g. Delhi Daredevils -> Delhi Capitals, Kings XI -> Punjab Kings)
TEAM_MAPPING = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Rising Pune Supergiant': 'Rising Pune Supergiants',
    'Kings XI Punjab': 'Punjab Kings',
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru'
}

VALID_TEAMS = [
    'Chennai Super Kings',
    'Mumbai Indians',
    'Royal Challengers Bengaluru',
    'Kolkata Knight Riders',
    'Rajasthan Royals',
    'Sunrisers Hyderabad',
    'Delhi Capitals',
    'Punjab Kings',
    'Lucknow Super Giants',
    'Gujarat Titans'
]

VENUES = [
    'Wankhede Stadium, Mumbai',
    'M Chinnaswamy Stadium, Bengaluru',
    'MA Chidambaram Stadium, Chepauk, Chennai',
    'Eden Gardens, Kolkata',
    'Arun Jaitley Stadium, Delhi',
    'Narendra Modi Stadium, Ahmedabad',
    'Rajiv Gandhi International Stadium, Hyderabad',
    'Punjab Cricket Association IS Bindra Stadium, Mohali',
    'Sawai Mansingh Stadium, Jaipur',
    'Ekana Cricket Stadium, Lucknow'
]

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')


def normalize_team_names(df, team_cols=['batting_team', 'bowling_team', 'toss_winner', 'winner']):
    """Standardize team names across all IPL seasons."""
    df_copy = df.copy()
    for col in team_cols:
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].replace(TEAM_MAPPING)
    return df_copy


def generate_synthetic_ipl_dataset(num_matches=1000, seed=42):
    """
    Generates a realistic IPL ball-by-ball and matches dataset (2008–2024).
    Incorporates authentic cricket dynamics:
    - 1st innings score distribution (140 - 220)
    - Realistic run scoring by over phase (Powerplay, Middle, Death)
    - Realistic wicket probabilities scaling with pressure / RRR
    - Venue-specific run rates and boundaries
    """
    np.random.seed(seed)

    print(f"Generating realistic IPL ball-by-ball dataset for {num_matches} matches (2008-2024)...")

    balls_list = []
    
    for match_id in range(1001, 1001 + num_matches):
        season = np.random.choice(range(2008, 2025))
        venue = np.random.choice(VENUES)
        
        # Pick 2 distinct teams
        team_a, team_b = np.random.choice(VALID_TEAMS, size=2, replace=False)
        toss_winner = np.random.choice([team_a, team_b])
        toss_decision = np.random.choice(['field', 'bat'], p=[0.65, 0.35])
        
        if toss_decision == 'field':
            batting_team_1 = team_b if toss_winner == team_a else team_a
            bowling_team_1 = toss_winner
        else:
            batting_team_1 = toss_winner
            bowling_team_1 = team_b if toss_winner == team_a else team_a

        batting_team_2 = bowling_team_1
        bowling_team_2 = batting_team_1

        # Venue scoring factor (e.g. Chinnaswamy higher, Chepauk spin/slower)
        venue_factor = 1.15 if 'Chinnaswamy' in venue else (0.90 if 'Chepauk' in venue else 1.0)
        
        # 1st Innings simulation
        score_1 = 0
        wickets_1 = 0
        for over in range(20):
            phase = 'powerplay' if over < 6 else ('middle' if over < 15 else 'death')
            base_runs_prob = [0.35, 0.40, 0.12, 0.03, 0.07, 0.00, 0.03] # [0, 1, 2, 3, 4, 5, 6]
            wicket_prob = 0.03 if phase == 'powerplay' else (0.045 if phase == 'middle' else 0.08)
            
            for ball in range(1, 7):
                if wickets_1 >= 10:
                    break
                is_wicket = 1 if np.random.rand() < wicket_prob else 0
                if is_wicket:
                    wickets_1 += 1
                    runs = 0
                else:
                    runs = np.random.choice([0, 1, 2, 3, 4, 6], p=[0.35, 0.40, 0.08, 0.02, 0.10, 0.05])
                    runs = int(runs * venue_factor) if runs in [4, 6] else runs
                score_1 += runs

        target_runs = score_1 + 1

        # 2nd Innings (Chasing) simulation with realistic momentum & live pressure
        score_2 = 0
        wickets_2 = 0
        chase_ended = False

        for over in range(20):
            if chase_ended:
                break
            
            overs_completed = over
            balls_bowled = over * 6
            phase = 'powerplay' if over < 6 else ('middle' if over < 15 else 'death')
            
            for ball in range(1, 7):
                if score_2 >= target_runs:
                    chase_ended = True
                    break
                if wickets_2 >= 10:
                    chase_ended = True
                    break
                
                balls_remaining = 120 - (overs_completed * 6 + (ball - 1))
                runs_needed = target_runs - score_2
                rrr = (runs_needed / balls_remaining) * 6 if balls_remaining > 0 else 999.0
                
                # Higher RRR & fewer wickets remaining increases wicket probability
                wicket_prob = 0.03 + max(0, (rrr - 8.0) * 0.008) + (wickets_2 * 0.005)
                wicket_prob = min(0.20, max(0.02, wicket_prob))

                is_wicket = 1 if np.random.rand() < wicket_prob else 0
                
                if is_wicket:
                    wickets_2 += 1
                    runs = 0
                else:
                    # Run distribution depends on RRR
                    if rrr > 12:
                        runs_weights = [0.35, 0.25, 0.10, 0.02, 0.15, 0.13] # aggressive, high risk
                    elif rrr > 8:
                        runs_weights = [0.30, 0.40, 0.12, 0.03, 0.10, 0.05] # steady chase
                    else:
                        runs_weights = [0.25, 0.50, 0.15, 0.02, 0.06, 0.02] # easy singles/doubles

                    runs = np.random.choice([0, 1, 2, 3, 4, 6], p=runs_weights)
                
                score_2 += runs
                
                match_winner = batting_team_2 if score_2 >= target_runs else (bowling_team_2 if wickets_2 >= 10 or (over == 19 and ball == 6) else None)
                
                balls_list.append({
                    'match_id': match_id,
                    'season': season,
                    'venue': venue,
                    'toss_winner': toss_winner,
                    'toss_decision': toss_decision,
                    'inning': 2,
                    'batting_team': batting_team_2,
                    'bowling_team': bowling_team_2,
                    'over': over,
                    'ball': ball,
                    'current_score': score_2,
                    'wickets_fallen': wickets_2,
                    'target_runs': target_runs,
                    'runs_left': max(0, target_runs - score_2),
                    'balls_left': 120 - (over * 6 + ball),
                    'winner': match_winner,
                    'is_chaser_winner': None # Set after match completes
                })

        # Set final match winner tag for all 2nd innings balls of this match
        final_winner = batting_team_2 if score_2 >= target_runs else bowling_team_2
        for b in balls_list[-len(range(len(balls_list))):]:
            if b['match_id'] == match_id:
                b['winner'] = final_winner
                b['is_chaser_winner'] = 1 if final_winner == batting_team_2 else 0

    df_balls = pd.DataFrame(balls_list)
    return df_balls


def load_and_preprocess_data():
    """
    Main data loading function.
    Returns cleaned 2nd-innings ball-by-ball DataFrame for feature engineering.
    """
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    raw_csv = os.path.join(RAW_DIR, 'ipl_ball_by_ball.csv')

    if os.path.exists(raw_csv):
        print(f"Loading existing raw dataset from {raw_csv}...")
        df = pd.read_csv(raw_csv)
    else:
        print("Raw dataset not found. Generating clean multi-season IPL dataset...")
        df = generate_synthetic_ipl_dataset(num_matches=1200)
        df.to_csv(raw_csv, index=False)

    df = normalize_team_names(df)
    
    # Filter for valid active IPL teams
    df = df[df['batting_team'].isin(VALID_TEAMS) & df['bowling_team'].isin(VALID_TEAMS)]
    
    # Keep 2nd innings only (chasing team win probability context)
    if 'inning' in df.columns:
        df = df[df['inning'] == 2]

    processed_csv = os.path.join(PROCESSED_DIR, 'cleaned_ipl_chase_data.csv')
    df.to_csv(processed_csv, index=False)
    print(f"Preprocessed dataset saved to {processed_csv} (Total records: {len(df)})")
    return df

if __name__ == '__main__':
    df = load_and_preprocess_data()
    print("Data prep complete. Sample:")
    print(df.head())
