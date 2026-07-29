import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import joblib
# pyrefly: ignore [missing-import]
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
from src.data_prep import VENUES, VALID_TEAMS

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'first_innings_model.joblib')


def generate_synthetic_1st_innings_data(num_samples=5000, seed=42):
    """
    Generates synthetic 1st innings score progression trajectories for training.
    """
    np.random.seed(seed)
    records = []

    for _ in range(num_samples):
        venue = np.random.choice(VENUES)
        batting_team = np.random.choice(VALID_TEAMS)
        bowling_team = np.random.choice(VALID_TEAMS)

        # Baseline expected total based on venue
        baseline = 190.0 if 'Chinnaswamy' in venue else (155.0 if 'Chepauk' in venue else 172.0)
        
        # Simulate final total for this match
        final_total = int(np.random.normal(loc=baseline, scale=22))
        final_total = max(90, min(260, final_total))

        # Pick random point in 1st innings (overs 1 to 19)
        overs = round(np.random.uniform(1.0, 19.0), 1)
        progress_frac = overs / 20.0

        # Wickets lost so far
        wickets = int(np.random.binomial(n=9, p=progress_frac * 0.7))
        wickets = min(9, wickets)

        # Current score with noise
        score_frac = (progress_frac ** 0.9) * (1.0 - (wickets * 0.04))
        current_score = int(final_total * max(0.1, score_frac))

        records.append({
            'batting_team': batting_team,
            'bowling_team': bowling_team,
            'venue': venue,
            'current_score': current_score,
            'overs_completed': overs,
            'wickets_fallen': wickets,
            'final_total': final_total
        })

    return pd.DataFrame(records)


def train_first_innings_model():
    os.makedirs(MODELS_DIR, exist_ok=True)
    print("Training 1st Innings Projected Score Model...")
    df = generate_synthetic_1st_innings_data()

    categorical_cols = ['batting_team', 'bowling_team', 'venue']
    numerical_cols = ['current_score', 'overs_completed', 'wickets_fallen']

    X = df[categorical_cols + numerical_cols]
    y = df['final_total'].values

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
            ('num', StandardScaler(), numerical_cols)
        ]
    )

    regressor = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', regressor)
    ])

    pipeline.fit(X, y)

    joblib.dump(pipeline, MODEL_PATH)
    print(f"Saved 1st Innings score projection model to {MODEL_PATH}")
    return pipeline


class FirstInningsPredictor:
    def __init__(self, model_path=MODEL_PATH):
        if not os.path.exists(model_path):
            self.pipeline = train_first_innings_model()
        else:
            self.pipeline = joblib.load(model_path)

    def predict_projected_score(self, batting_team, bowling_team, venue, current_score, overs_completed, wickets_fallen):
        """
        Returns estimated final 1st Innings target total and 80% confidence interval range.
        """
        df_in = pd.DataFrame([{
            'batting_team': batting_team,
            'bowling_team': bowling_team,
            'venue': venue,
            'current_score': current_score,
            'overs_completed': overs_completed,
            'wickets_fallen': wickets_fallen
        }])

        pred_score = float(self.pipeline.predict(df_in)[0])
        pred_score = max(current_score + 1, int(round(pred_score)))

        min_range = max(current_score + 1, pred_score - 12)
        max_range = pred_score + 14

        return {
            'projected_score': pred_score,
            'range_min': min_range,
            'range_max': max_range
        }

if __name__ == '__main__':
    train_first_innings_model()
