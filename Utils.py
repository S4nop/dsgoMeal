from datetime import date


def get_year_month_day():
    today = date.today()
    year = today.year
    month = today.month
    day = today.day

    return {'year': year, 'month': month, 'day': day}