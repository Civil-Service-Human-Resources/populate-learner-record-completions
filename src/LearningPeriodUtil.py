from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_current_learning_period(required_by: str, frequency: str):
    required_by_date = datetime.strptime(required_by, "%Y-%m-%dT%H:%M:%S")
    frequency_years = int(list(frequency)[1])

    while required_by_date < datetime.now():
        required_by_date += relativedelta(years=frequency_years)
    return required_by_date - relativedelta(years=frequency_years)