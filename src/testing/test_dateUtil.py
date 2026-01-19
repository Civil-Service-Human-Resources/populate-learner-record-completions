import modules.utils.DateUtil as DateUtil

def test_get_date_partition_name_returns_correct_partition_name_for_date():
    date = "2025-01-02T01:00:00"
    partition_name = DateUtil.get_date_partition_name(date)

    assert partition_name == "course_completion_events_2025_1_2"

def test_get_partition_dates_returns_correct_start_and_end_dates_for_date():
    date = "2024-05-10T01:00:00"

    partition_dates = DateUtil.get_partition_dates(date)

    assert partition_dates["start_date"] == "2024-05-10"
    assert partition_dates["end_date"] == "2024-05-11"
