import json
import pandas as pd

with open("./data/plan.json", "r") as plan_file:
    incomplete_records = json.load(plan_file)

data_frame = pd.DataFrame(incomplete_records)
data_frame["completion_timestamp"] = pd.to_datetime(data_frame["completion_timestamp"])
data_frame["completion_month"] = data_frame["completion_timestamp"].dt.to_period("M")
monthly_counts = data_frame.groupby("completion_month").size()
print(monthly_counts.to_frame(name="incomplete_records").to_markdown())