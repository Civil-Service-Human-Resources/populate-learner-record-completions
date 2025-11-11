from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_current_learning_period(required_by: str, frequency: str = None):
    required_by_date = datetime.strptime(required_by, "%Y-%m-%dT%H:%M:%S")

    if frequency is None:
        return datetime.fromtimestamp(0)

    frequency_period = get_years_and_months_from_frequency(frequency)
    while required_by_date < datetime.now():
        required_by_date += relativedelta(years=frequency_period["years"], months=frequency_period["months"])

    required_by_date += relativedelta(minutes=1)
    return required_by_date - relativedelta(years=frequency_period["years"], months=frequency_period["months"])

def get_years_and_months_from_frequency(frequency: str):
    frequency_tokens = list(frequency)

    if len(frequency_tokens) == 5 and frequency_tokens[4] == 'M' and frequency_tokens[2] == 'Y':
        return {
            "years": int(frequency_tokens[1]),
            "months": int(frequency_tokens[3])
        }
    elif len(frequency_tokens) == 3:
        if(frequency_tokens[2] == 'Y'):
            return {
                "years": int(frequency_tokens[1]),
                "months": 0
            }
        elif(frequency_tokens[2] == 'M'):
            return {
                "years": 0,
                "months": int(frequency_tokens[1])
            }
    
    raise ValueError("Invalid frequency format")