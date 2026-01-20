import modules.utils.LearningPeriodUtil as LearningPeriodUtil
from datetime import datetime

def test_get_learning_period_for_date_returns_start_date_0_and_end_date_as_current_date_if_required_by_and_frequency_are_None(mocker):
    mocker.patch.object(LearningPeriodUtil, 'get_date_now', return_value=datetime(2026, 1, 1, 0, 0, 0, 0))

    learning_period = LearningPeriodUtil.get_learning_period_for_date("2026-01-01T00:00:00", None, None)

    assert learning_period["start_date"] == datetime.fromtimestamp(0)
    assert learning_period["end_date"] == datetime(2026, 1, 1, 0, 0, 0, 0)

def test_get_learning_period_for_date_returns_start_date_0_and_end_date_as_required_by_date_if_required_by_is_not_None_and_frequency_is_None():
    learning_period = LearningPeriodUtil.get_learning_period_for_date("2025-01-01T00:00:00", "2025-12-01T00:00:00", None)

    assert learning_period["start_date"] == datetime.fromtimestamp(0)
    assert learning_period["end_date"] == datetime(2025, 12, 1, 0, 0, 0, 0)

def test_get_learning_period_for_date_returns_start_date_0_and_end_date_as_current_date_if_target_date_is_later_than_required_by_date(mocker):
    mocker.patch.object(LearningPeriodUtil, 'get_date_now', return_value=datetime(2026, 1, 1, 0, 0, 0, 0))

    learning_period = LearningPeriodUtil.get_learning_period_for_date("2026-01-01T00:00:00", "2025-12-01T00:00:00", None)


    assert learning_period["start_date"] == datetime.fromtimestamp(0)
    assert learning_period["end_date"] == datetime(2026, 1, 1, 0, 0, 0, 0)

def test_get_learning_period_for_date_returns_the_correct_current_learning_period_if_required_by_is_not_None_and_frequency_is_P1Y():
    learning_period = LearningPeriodUtil.get_learning_period_for_date("2026-01-01T00:00:00", "2024-03-31T00:00:00", 'P1Y')

    assert learning_period["start_date"] == datetime(2025, 3, 31, 0, 1)
    assert learning_period["end_date"] == datetime(2026, 3, 31, 0, 0)

def test_get_learning_period_for_date_returns_the_correct_current_learning_period_if_required_by_is_not_None_and_frequency_is_P6M():
    learning_period = LearningPeriodUtil.get_learning_period_for_date("2026-01-01T00:00:00", "2024-03-31T00:00:00", 'P6M')

    assert learning_period["start_date"] == datetime(2025, 9, 30, 0, 1)
    assert learning_period["end_date"] == datetime(2026, 3, 30, 0, 0)