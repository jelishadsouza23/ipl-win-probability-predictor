import streamlit as st
import pickle
import pandas as pd

# Page setup
st.set_page_config(
    page_title="IPL Win Probability Predictor",
    page_icon="🏏",
    layout="centered"
)

st.title("🏏 IPL Win Probability Predictor")
st.markdown("Predict the win percentage of the chasing team in real-time!")

# Teams & Cities Options
teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bengaluru',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals'
]

cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Cuttack', 'Ahmedabad', 'Visakhapatnam', 'Dharamshala',
    'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah', 'Dubai', 'Lucknow'
]

# Form Inputs
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select Batting Team (Chasing)', sorted(teams))

with col2:
    bowling_team = st.selectbox('Select Bowling Team', sorted(teams))

selected_city = st.selectbox('Select Host City', sorted(cities))
target = st.number_input('Target Score', min_value=1, max_value=300, value=180, step=1)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score', min_value=0, max_value=300, value=100, step=1)

with col4:
    overs = st.number_input('Overs Completed', min_value=0.0, max_value=20.0, value=10.0, step=0.1)

with col5:
    wickets = st.number_input('Wickets Lost', min_value=0, max_value=10, value=3, step=1)

# Prediction Logic
if st.button('Predict Probability', type="primary"):
    if batting_team == bowling_team:
        st.error("Batting team and Bowling team cannot be the same.")
    elif overs == 0:
        st.error("Overs completed must be greater than 0.")
    elif score > target:
        st.success(f"{batting_team} has already won the match!")
    else:
        # Calculate derived metrics
        runs_left = target - score
        balls_left = 120 - int(overs * 6)
        wickets_remaining = 10 - wickets
        crr = score / overs
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_remaining],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        try:
            # Load model relative to repository root
            pipe = pickle.load(open('../models/pipe.pkl', 'rb'))
            result = pipe.predict_proba(input_df)

            loss_prob = round(result[0][0] * 100)
            win_prob = round(result[0][1] * 100)

            st.divider()
            st.subheader("Predicted Win Probabilities")

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric(label=batting_team, value=f"{win_prob}%")
            with res_col2:
                st.metric(label=bowling_team, value=f"{loss_prob}%")

            st.progress(win_prob / 100)

        except FileNotFoundError:
            st.error("Model file not found! Make sure `pipe.pkl` is located inside the `models/` folder.")
