import pickle
import pandas as pd

def get_reporting_data_for_user_and_date(user_id: str, date: str):
    all_completions = get_reporting_data()
    df = pd.DataFrame(all_completions, columns=[
        "user_id",
        "user_email",
        "organisation_id",
        "organisation_name",
        "profession_id",
        "profession_name",
        "grade_id",
        "grade_name",
        "event_timestamp"
    ])
    user_completions = df[df['user_id'] == user_id]

    if user_completions.empty:
        return None

    df_sorted = (user_completions.assign(distance=(df["event_timestamp"] - pd.Timestamp(date)).abs())
        .sort_values("distance")
        .drop(columns="distance")
    )
    return tuple(df_sorted.iloc[0][1:-1])

def get_reporting_data():
    with open("/app-data/reporting_completions.pkl", "rb") as file:
        reporting_data = pickle.load(file)
    return reporting_data