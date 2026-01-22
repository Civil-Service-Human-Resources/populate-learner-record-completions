import pickle
import pandas as pd

def get_reporting_data_for_user_and_date(df, user_id: str, date: str):
    user_completions = df[df['user_id'] == user_id]

    if user_completions.empty:
        return None

    df_sorted = (user_completions.assign(distance=(user_completions["event_timestamp"] - pd.Timestamp(date)).abs())
        .sort_values("distance")
        .drop(columns="distance")
    )
    return tuple(df_sorted.iloc[0][1:-1])

def get_reporting_data():
    with open("/app-data/reporting_completions.pkl", "rb") as file:
        reporting_data = pickle.load(file)
    return reporting_data