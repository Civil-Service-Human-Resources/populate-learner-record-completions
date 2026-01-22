import pandas as pd

def get_mandatory_module_completions_for_user_and_course(df, user_id, course_id, start_date, end_date):
    filtered_df = df.loc[(user_id, course_id)]
    filtered_df = filtered_df[filtered_df["completion_date"].between(pd.Timestamp(start_date), pd.Timestamp(end_date))]
    return filtered_df

def get_course_completion_events_for_user_and_course(df, user_id, course_id, learning_period_start, learning_period_end):
    try:
        filtered_df = df.loc[(user_id, course_id)]
        filtered_df_for_time_period = filtered_df[filtered_df["event_timestamp"].between(pd.Timestamp(learning_period_start), pd.Timestamp(learning_period_end))]
        return filtered_df_for_time_period
    except Exception as e:
        return None