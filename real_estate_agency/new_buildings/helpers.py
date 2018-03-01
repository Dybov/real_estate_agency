import datetime

from django.utils.translation import ugettext as _


def get_quarter(date, empty=''):
    answer = {
        'quarter': empty, 
        'year': empty,
        'verbose_name': empty,
    }
    if isinstance(date, datetime.date):
        qrtr = (date.month-1)//3+1
        answer['quarter'] = qrtr
        answer['year'] = date.year
        answer['verbose_name'] = _('{quarter} квартал {year}').format(**answer)
    return answer

def last_day_of_month(any_day):
    next_month = any_day.replace(
        day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def get_quarter_verbose(date, empty=''):
    return get_quarter(date, empty)['verbose_name']