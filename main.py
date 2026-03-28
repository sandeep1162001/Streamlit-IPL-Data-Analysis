import streamlit as st

# Core Libraries 
import numpy as np
import pandas as pd
import warnings

# Visualization Libraries 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from wordcloud import WordCloud


# Data Loading and Preprocessing
warnings.filterwarnings('ignore')
df = pd.read_csv('IPL_cleaned.csv')



# Functions 
# Function to analyze Bowler vs. Batsman
def h2h(batsman, bowler):

    if not str(batsman) or not str(bowler):
        return   # stop execution

    h2h_df = df[(df['batter'] == str(batsman)) & (df['bowler'] == str(bowler))]
    if h2h_df.empty:
        st.warning(f"No encounters found between {batsman} and {bowler}.")
        return

    # Batting stats
    runs = h2h_df['runs_batter'].sum()
    balls = len(h2h_df)
    dismissals = h2h_df['striker_out'].sum()
    batting_strike_rate = (runs / balls) * 100 if balls > 0 else 0
    batting_average = runs / dismissals if dismissals > 0 else runs
    fours = (h2h_df['runs_batter'] == 4).sum()
    sixes = (h2h_df['runs_batter'] == 6).sum()
    boundary_runs = fours * 4 + sixes * 6
    boundary_pct = ((fours + sixes) / balls) * 100
    dot_balls = (h2h_df['runs_batter'] == 0).sum()
    dot_pct = (dot_balls / balls) * 100
    singles = (h2h_df['runs_batter'] == 1).sum()
    bowling_economy = (runs*6)/balls
    bowling_average = runs/dismissals if dismissals > 0 else runs
    bowling_strike_rate = balls/dismissals

    st.subheader(f" Head-to-Head: {batsman} vs. {bowler} ")

    col1,col2 = st.columns(2)
    with col1:
        st.write(f"Runs Scored: {runs}")
        st.write(f"Balls Faced: {balls}")
        st.write(f"Batsman Strike Rate: {batting_strike_rate:.2f}")
        st.write(f"Batting Average: {batting_average:.2f}")
        st.write(f"Fours: {fours}")
        st.write(f"Sixes: {sixes}")
        st.write(f"Boundary runs: {boundary_runs}")
        st.write(f"Single (Strike Rotation): {singles}")

    with col2:
        st.write(f"Dismissals: {dismissals}")
        st.write(f"Bowling Strike rate: {bowling_strike_rate:.2f}")      
        st.write(f"Bowling Economy: {bowling_economy:.2f}")
        st.write(f"Bowling Average: {bowling_average:.2f}")
        st.write(f"Boundary Percentage: {boundary_pct:.2f} %")
        st.write(f"Dot Balls: {dot_balls}")
        st.write(f"Dot percentage: {dot_pct:.2f} %")



# Function to analyze Team vs. Batsman
def team_vs_batsman(batsman, team):

    if not str(batsman) or not str(team):
        return   # stop execution

    team_vs_batsman_df = df[(df['batter'] == str(batsman)) & (df['bowling_team'] == str(team))]
    if team_vs_batsman_df.empty:
        st.warning(f"No encounters found between {batsman} and {team}.")
        return

    runs = team_vs_batsman_df['runs_batter'].sum()
    balls = len(team_vs_batsman_df)
    dismissals = team_vs_batsman_df['striker_out'].sum()
    strike_rate = (runs / balls) * 100 if balls > 0 else 0
    average = runs / dismissals if dismissals > 0 else runs
    fours = (team_vs_batsman_df['runs_batter'] == 4).sum()
    sixes = (team_vs_batsman_df['runs_batter'] == 6).sum()
    boundary_runs = fours * 4 + sixes * 6
    boundary_pct = ((fours + sixes) / balls) * 100
    dot_balls = (team_vs_batsman_df['runs_batter'] == 0).sum()
    dot_pct = (dot_balls / balls) * 100
    singles = (team_vs_batsman_df['runs_batter'] == 1).sum()



    st.subheader(f" Head-to-Head: {batsman} vs. {team} ")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Runs Scored: {runs}")
        st.write(f"Balls Faced: {balls}")
        st.write(f"Dismissals: {dismissals}")
        st.write(f"Strike rate: {strike_rate:.2f}")
        st.write(f"Average: {average:.2f}")
        st.write(f"Single (Strike Rotation): {singles}")
    with col2:
        st.write(f"Fours: {fours}")
        st.write(f"Sixes: {sixes}")
        st.write(f"Boundary runs: {boundary_runs}")
        st.write(f"Boundary Percentage: {boundary_pct:.2f} %")
        st.write(f"Dot Balls: {dot_balls}")
        st.write(f"Dot percentage: {dot_pct:.2f} %")


# Function to analyze Team vs. Bowler
def team_vs_bowler(bowler, team):

    if not str(bowler) or not str(team):
        return   # stop execution

    team_vs_bowler_df = df[(df['bowler'] == str(bowler)) & (df['batting_team'] == str(team))]
    if team_vs_bowler_df.empty:
        st.warning(f"No encounters found between {bowler} and {team}.")
        return

    runs = team_vs_bowler_df['runs_batter'].sum()
    balls = len(team_vs_bowler_df)
    dismissals = team_vs_bowler_df['striker_out'].sum()
    economy = (runs*6)/balls
    average = runs/dismissals if dismissals > 0 else runs
    strike_rate = balls/dismissals
    overs = balls // 6 + (balls % 6) / 10
    dot_balls = team_vs_bowler_df[
            (team_vs_bowler_df['runs_total'] == 0) &
            (team_vs_bowler_df['extra_type'].isna())
        ].shape[0]
    dot_percentage = (dot_balls / balls) * 100
    fours = team_vs_bowler_df[team_vs_bowler_df['runs_batter']== 4].shape[0]
    sixes = team_vs_bowler_df[team_vs_bowler_df['runs_batter']== 6].shape[0]
    boundary_percent = (fours + sixes) / balls * 100

    st.subheader(f" Head-to-Head: {bowler} vs. {team} ")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Wickets Taken: {dismissals}")
        st.write(f"Runs Given: {runs}")
        st.write(f"Balls Delivered: {balls}")
        st.write(f"Economy : {economy:.2f}")
        st.write(f"Average : {average:.2f}")
        st.write(f"Strike Rate : {strike_rate:.2f}")
    with col2:
        st.write(f"Over : {overs}")
        st.write(f"Dot balls : {dot_balls}")
        st.write(f"Dot balls percent : {dot_percentage:.2f} %")
        st.write(f"Fours Given : {fours}")
        st.write(f"sixes Given : {sixes}")
        st.write(f"Boundary percent : {boundary_percent:.2f} %")



st.markdown("<h1 style='text-align: center;'>IPL Data Analysis</h1> ",unsafe_allow_html=True)
st.markdown('---')

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Analysis Parameters</h2>",unsafe_allow_html=True)
    st.markdown('---')

    st.markdown("## Head-to-Head Analysis")
    h2h_batsman = st.selectbox('Select Batsman',np.sort(df['batter'].unique()),key='h2h_batsman')
    h2h_bowler = st.selectbox('Select Bowlwer',np.sort(df['bowler'].unique()),key='h2h_bowler')
    analyze_1 = st.button("Analyze",key='h2h')
    st.markdown('---')

    st.markdown("## Team vs batsman Analysis")
    tvb_batsman = st.selectbox('Select Batsman',np.sort(df['batter'].unique()),key='team_vs_batsman_batsman')
    tvb_team = st.selectbox('Select Team',np.sort(df['batting_team'].unique()),key='team_vs_batsman_team')
    analyze_2 = st.button("Analyze",key='team_vs_batsman')
    st.markdown('---')

    st.markdown("## Team vs bowler Analysis")
    tv_bowler = st.selectbox('Select Bowler',np.sort(df['bowler'].unique()),key='team_vs_bowler_bowler')
    tv_team = st.selectbox('Select Team',np.sort(df['batting_team'].unique()),key='team_vs_bowler_team')
    analyze_3 = st.button("Analyze",key='team_vs_bowler')
    st.markdown('---')

if analyze_1:
    h2h(h2h_batsman,h2h_bowler)

if analyze_2:
    team_vs_batsman(tvb_batsman,tvb_team)

if analyze_3:
    team_vs_bowler(tv_bowler,tv_team)