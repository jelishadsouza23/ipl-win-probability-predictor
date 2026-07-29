import os
import sys
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
from typing import List
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException, status
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from fastapi.staticfiles import StaticFiles

# Add parent dir to path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.schemas import PredictRequest, PredictResponse, MetadataResponse, TeamInfo, VenueInfo
from src.predict import WinPredictor
from src.data_prep import VALID_TEAMS, VENUES, generate_synthetic_ipl_dataset
from src.feature_engineering import compute_derived_features

app = FastAPI(
    title="IPL Win Probability Predictor API",
    description="Machine Learning API for predicting live IPL 2nd innings match win probabilities",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_root():
    # pyrefly: ignore [missing-import]
    from fastapi.responses import FileResponse
    index_file = os.path.join(STATIC_DIR, 'index.html')
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "IPL Win Probability Predictor API is active."}

# Lazy loading of WinPredictor singleton
predictor = None

def get_predictor():
    global predictor
    if predictor is None:
        try:
            predictor = WinPredictor()
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model artifact not trained yet. {str(e)}"
            )
    return predictor


TEAM_METADATA = [
    {"name": "Chennai Super Kings", "short_name": "CSK", "primary_color": "#FFFF00", "secondary_color": "#002B49"},
    {"name": "Mumbai Indians", "short_name": "MI", "primary_color": "#004BA0", "secondary_color": "#D4AF37"},
    {"name": "Royal Challengers Bengaluru", "short_name": "RCB", "primary_color": "#EC1C24", "secondary_color": "#000000"},
    {"name": "Kolkata Knight Riders", "short_name": "KKR", "primary_color": "#3A225D", "secondary_color": "#F3A812"},
    {"name": "Rajasthan Royals", "short_name": "RR", "primary_color": "#EA1B85", "secondary_color": "#254AA5"},
    {"name": "Sunrisers Hyderabad", "short_name": "SRH", "primary_color": "#F26522", "secondary_color": "#000000"},
    {"name": "Delhi Capitals", "short_name": "DC", "primary_color": "#00008B", "secondary_color": "#DC143C"},
    {"name": "Punjab Kings", "short_name": "PBKS", "primary_color": "#DD1D25", "secondary_color": "#B19456"},
    {"name": "Lucknow Super Giants", "short_name": "LSG", "primary_color": "#0057B8", "secondary_color": "#E30613"},
    {"name": "Gujarat Titans", "short_name": "GT", "primary_color": "#1B2133", "secondary_color": "#DBBE6E"}
]


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "IPL Win Probability Predictor API"}


@app.get("/api/metadata", response_model=MetadataResponse)
def get_metadata():
    teams = [TeamInfo(**t) for t in TEAM_METADATA]
    venues = [VenueInfo(name=v, city=v.split(',')[-1].strip() if ',' in v else v) for v in VENUES]
    return MetadataResponse(
        teams=teams,
        venues=venues,
        default_venue=VENUES[0]
    )


@app.post("/api/predict", response_model=PredictResponse)
def predict_win_probability(req: PredictRequest):
    pred = get_predictor()
    try:
        match_dict = req.model_dump()
        result = pred.predict_match_state(match_dict)
        return PredictResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating win probability: {str(e)}"
        )


@app.get("/api/sample-matches")
def get_sample_matches():
    """
    Returns curated historical IPL thriller matches for the over-by-over live simulator feature.
    """
    sample_matches = [
        {
            "id": "match_2023_final",
            "title": "CSK vs GT (IPL 2023 Final Thriller)",
            "batting_team": "Chennai Super Kings",
            "bowling_team": "Gujarat Titans",
            "venue": "Narendra Modi Stadium, Ahmedabad",
            "target": 171,
            "overs": 15,
            "description": "Rain-affected target chase with Jadeja finishing off on the final ball!"
        },
        {
            "id": "match_2019_final",
            "title": "MI vs CSK (IPL 2019 Final - 1 Run Win)",
            "batting_team": "Chennai Super Kings",
            "bowling_team": "Mumbai Indians",
            "venue": "Rajiv Gandhi International Stadium, Hyderabad",
            "target": 150,
            "overs": 20,
            "description": "Lasith Malinga's iconic slow ball on the final delivery sealing MI's 4th title."
        },
        {
            "id": "match_rcb_kkr",
            "title": "RCB vs KKR (High-Scoring Eden Gardens Chase)",
            "batting_team": "Royal Challengers Bengaluru",
            "bowling_team": "Kolkata Knight Riders",
            "venue": "Eden Gardens, Kolkata",
            "target": 205,
            "overs": 20,
            "description": "Classic 200+ run chase with wild win probability swings."
        }
    ]
    return sample_matches


@app.get("/api/simulate-match/{match_id}")
def simulate_historical_match(match_id: str):
    """
    Generates a ball-by-ball simulated chase replay with live win probability recalculated on every delivery.
    """
    pred = get_predictor()

    # Configure match parameters based on selected sample
    if match_id == "match_2023_final":
        batting_team = "Chennai Super Kings"
        bowling_team = "Gujarat Titans"
        venue = "Narendra Modi Stadium, Ahmedabad"
        target_runs = 171
        total_overs = 15
    elif match_id == "match_2019_final":
        batting_team = "Chennai Super Kings"
        bowling_team = "Mumbai Indians"
        venue = "Rajiv Gandhi International Stadium, Hyderabad"
        target_runs = 150
        total_overs = 20
    else:
        batting_team = "Royal Challengers Bengaluru"
        bowling_team = "Kolkata Knight Riders"
        venue = "Eden Gardens, Kolkata"
        target_runs = 205
        total_overs = 20

    # Simulate realistic ball-by-ball trajectory
    np.random.seed(hash(match_id) % 10000)
    score = 0
    wickets = 0
    ball_records = []

    for over in range(total_overs):
        for ball in range(1, 7):
            if score >= target_runs or wickets >= 10:
                break

            balls_left = (total_overs * 6) - (over * 6 + ball)
            runs_left = target_runs - score
            rrr = (runs_left * 6 / balls_left) if balls_left > 0 else 999.0

            # Dynamic event probability based on RRR
            w_prob = 0.035 + max(0, (rrr - 9.0) * 0.008) + (wickets * 0.004)
            is_wicket = 1 if np.random.rand() < w_prob else 0

            if is_wicket:
                wickets += 1
                runs_ball = 0
                event_type = "W"
            else:
                runs_ball = int(np.random.choice([0, 1, 2, 4, 6], p=[0.35, 0.40, 0.10, 0.10, 0.05]))
                event_type = str(runs_ball)

            score += runs_ball
            overs_completed = round(over + (ball / 6.0), 1)

            # Predict probability at this ball
            match_state = {
                "batting_team": batting_team,
                "bowling_team": bowling_team,
                "venue": venue,
                "current_score": score,
                "wickets_fallen": wickets,
                "overs_completed": overs_completed,
                "target_runs": target_runs,
                "toss_winner": batting_team,
                "toss_decision": "field"
            }

            p_res = pred.predict_match_state(match_state)

            ball_records.append({
                "over": over,
                "ball": ball,
                "overs_completed": overs_completed,
                "runs_ball": runs_ball,
                "event_type": event_type,
                "total_score": score,
                "wickets": wickets,
                "runs_left": max(0, target_runs - score),
                "balls_left": max(0, (total_overs * 6) - (over * 6 + ball)),
                "chasing_win_prob": p_res["chasing_team_win_prob"],
                "defending_win_prob": p_res["defending_team_win_prob"],
                "crr": p_res["crr"],
                "rrr": p_res["rrr"]
            })

    return {
        "match_id": match_id,
        "batting_team": batting_team,
        "bowling_team": bowling_team,
        "venue": venue,
        "target_runs": target_runs,
        "total_overs": total_overs,
        "ball_by_ball": ball_records
    }
