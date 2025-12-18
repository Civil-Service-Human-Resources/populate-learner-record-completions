from datetime import datetime, timedelta

def get_date_partition_name(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    return f"course_completion_events_{date.year}_{date.month}_{date.day}"

def get_partition_dates(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    start_date = date.strftime("%Y-%m-%d")
    next_day = date + timedelta(days=1)
    end_date = next_day.strftime("%Y-%m-%d")
    return {
        "start_date": start_date,
        "end_date": end_date
    }

def get_as_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

def get_date_now_as_string():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")