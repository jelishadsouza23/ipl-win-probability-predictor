import os
# pyrefly: ignore [missing-import]
import joblib
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
from src.feature_engineering import compute_derived_features

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'ipl_win_probability_model.joblib')


class WinPredictor:
    def __init__(self, model_path=MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Please run src/train.py first.")
        
        artifact = joblib.load(model_path)
        self.pipeline = artifact['pipeline']
        self.model_name = artifact.get('model_name', 'IPL Model')
        self.categorical_cols = artifact['categorical_cols']
        self.numerical_cols = artifact['numerical_cols']

    def predict_match_state(self, match_state_dict):
        """
        Takes match situation dictionary and returns win probabilities and key stats.
        Expected keys:
        - batting_team, bowling_team, venue
        - current_score, wickets_fallen, overs_completed, target_runs
        - toss_winner (optional)
        """
        df_input = pd.DataFrame([match_state_dict])
        
        # Calculate over and ball breakdown if only overs_completed given
        if 'over' not in df_input.columns or 'ball' not in df_input.columns:
            overs_val = float(match_state_dict['overs_completed'])
            over = int(overs_val)
            ball = int(round((overs_val - over) * 10))
            if ball >= 6:
                over += 1
                ball = 0
            df_input['over'] = over
            df_input['ball'] = ball
            df_input['overs_completed'] = over + (ball / 6.0)

        # Compute derived metrics
        df_feat = compute_derived_features(df_input)

        # Predict probability
        chasing_win_prob = float(self.pipeline.predict_proba(df_feat)[0, 1])
        defending_win_prob = float(1.0 - chasing_win_prob)

        row = df_feat.iloc[0]

        return {
            'batting_team': match_state_dict['batting_team'],
            'bowling_team': match_state_dict['bowling_team'],
            'chasing_team_win_prob': round(chasing_win_prob * 100, 2),
            'defending_team_win_prob': round(defending_win_prob * 100, 2),
            'current_score': int(row['current_score']),
            'wickets_fallen': int(row['wickets_fallen']),
            'wickets_remaining': int(row['wickets_remaining']),
            'overs_completed': round(float(row['overs_completed']), 1),
            'balls_left': int(row['balls_left']),
            'target_runs': int(row['target_runs']),
            'runs_left': int(row['runs_left']),
            'crr': round(float(row['crr']), 2),
            'rrr': round(float(row['rrr']), 2),
            'phase': row['phase']
        }
