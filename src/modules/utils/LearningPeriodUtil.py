from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_learning_period_for_date(target_date: str, required_by: str = None, frequency: str = None):
    target_date = datetime.strptime(target_date, "%Y-%m-%dT%H:%M:%S")
    required_by_date = datetime.strptime(required_by, "%Y-%m-%dT%H:%M:%S") if required_by is not None else None

    if required_by is None and frequency is None:
        return {
            "start_date": datetime.fromtimestamp(0),
            "end_date": get_date_now()
            }

    if required_by is not None and frequency is None:
        return {
            "start_date": datetime.fromtimestamp(0),
            "end_date": required_by_date if required_by_date > target_date else get_date_now()
        }

    frequency_period = get_years_and_months_from_frequency(frequency)

    if required_by_date > target_date:
        while required_by_date > target_date + relativedelta(minutes=1):
            required_by_date -= relativedelta(years=frequency_period["years"], months=frequency_period["months"])

        return {
            "start_date": required_by_date,
            "end_date": required_by_date + relativedelta(years=frequency_period["years"], months=frequency_period["months"])
        }
    else:
        while required_by_date < target_date:
            required_by_date += relativedelta(years=frequency_period["years"], months=frequency_period["months"])

        required_by_date += relativedelta(minutes=1)
        learning_period_start_date = required_by_date - relativedelta(years=frequency_period["years"], months=frequency_period["months"])

    return {
        "start_date": learning_period_start_date,
        "end_date": required_by_date - relativedelta(minutes=1)
    }

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

def get_date_now():
    return datetime.now()