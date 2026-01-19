import pandas as pd
import json
import pickle

with open("/app-data/plan.json", "r") as plan_file:
    incomplete_records = json.load(plan_file)

def get_total_incomplete_records():
    return len(incomplete_records)

def get_analytics_by_month():
    data_frame = pd.DataFrame(incomplete_records)
    data_frame["completion_timestamp"] = pd.to_datetime(data_frame["completion_timestamp"])
    data_frame["completion_month"] = data_frame["completion_timestamp"].dt.to_period("M")
    monthly_counts = data_frame.groupby("completion_month").size()
    return monthly_counts.to_frame(name="incomplete_records")

def get_analytics_by_course():
    courses = pickle.load(open("/app-data/courses.pkl", "rb"))
    courses_df = pd.DataFrame(courses)

    data_frame = pd.DataFrame(incomplete_records)
    course_counts = data_frame.groupby("course_id").size()
    course_counts = course_counts.sort_values(ascending=False)
    course_counts = course_counts.to_frame(name="incomplete_records")

    merged = pd.merge(course_counts, courses_df, left_on="course_id", right_on="id", how="left")
    merged["title"] = merged["title"].str[:50]

    return merged[["title", "incomplete_records"]]