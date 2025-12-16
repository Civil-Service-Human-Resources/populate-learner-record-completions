import json
import pandas as pd
import pickle

with open("./data/plan.json", "r") as plan_file:
    incomplete_records = json.load(plan_file)

data_frame = pd.DataFrame(incomplete_records)
course_counts = data_frame.groupby("course_id").size()
course_counts = course_counts.sort_values(ascending=False)
course_counts = course_counts.to_frame(name="incomplete_records")

courses = pickle.load(open("data/courses.pkl", "rb"))
courses_df = pd.DataFrame(courses)

merged = pd.merge(course_counts, courses_df, left_on="course_id", right_on="id", how="left")
merged["title"] = merged["title"].str[:50]

print(merged[["incomplete_records", "title"]].to_markdown())