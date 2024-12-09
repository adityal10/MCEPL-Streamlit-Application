import numpy as np
import pandas as pd


def prepare_data(df):
    del_cols = ['Time', 'Day', 'Referee', 'Attendance']
    df = df.drop(del_cols, axis=1)
    df = df.rename(columns={'Team': 'home_team', 'Opponent': 'away_team'})
    df = df[['Date', 'Round', 'Venue', 'home_team', 'away_team', 'GF', 'GA', 'Result', 'xG', 'xGA', 'Possession', 'Captain', 'Formation']]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date').reset_index(drop=True)
    return df


def calculate_transition_matrix(team, df, venue='Home'):
    filtered = df[(df['home_team'] == team) & (df['Venue'] == venue)]
    filtered = filtered.sort_values(by=['Date'])
    filtered['Previous_Match_State'] = filtered['Result'].shift(1)
    filtered = filtered.dropna(subset=['Previous_Match_State'])
    transition_counts = filtered.groupby(['Previous_Match_State', 'Result']).size().reset_index(name='Count')
    transition_matrix = transition_counts.pivot_table(index='Previous_Match_State', columns='Result', values='Count', fill_value=0)
    return transition_matrix.div(transition_matrix.sum(axis=1), axis=0)


def simulate_matches(transition_matrix, num_matches, initial_state='W'):
    points = 0
    current_state = initial_state

    for _ in range(num_matches):
        if current_state in transition_matrix.index:
            current_state = np.random.choice(transition_matrix.columns, p=transition_matrix.loc[current_state])
        else:
            current_state = np.random.choice(transition_matrix.columns)
        points += 3 if current_state == 'W' else 1 if current_state == 'D' else 0

    return points


def predict_team_points(team, df, remaining_home_matches, remaining_away_matches):
    home_matrix = calculate_transition_matrix(team, df, venue='Home')
    away_matrix = calculate_transition_matrix(team, df, venue='Away')

    home_points = simulate_matches(home_matrix, remaining_home_matches)
    away_points = simulate_matches(away_matrix, remaining_away_matches)

    return home_points + away_points


def calculate_final_points(df, remaining_home_matches=19, remaining_away_matches=19):
    teams = df['home_team'].unique()
    predictions = []

    for team in teams:
        predicted_points = predict_team_points(team, df, remaining_home_matches, remaining_away_matches)
        actual_points = df[df['home_team'] == team].apply(
            lambda x: 3 if x['Result'] == 'W' else 1 if x['Result'] == 'D' else 0, axis=1).sum()
        # print(actual_points)
        predictions.append({'Team': team, 'EPLPoints': actual_points, 'MCPoints': predicted_points})

    return pd.DataFrame(predictions).sort_values(by='EPLPoints', ascending=False).reset_index(drop=True)
