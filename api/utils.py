from django.db.models import fields, Subquery
from datetime import timedelta, date


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def last_day_of_month(any_day):
    next_month = any_day.replace(
        day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)
