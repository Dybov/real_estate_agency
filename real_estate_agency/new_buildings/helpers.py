import datetime

from django.utils.translation import ugettext as _


def get_quarter(date):
    qrtr = (date.month-1)//3+1
    answer = {
        'quarter':qrtr, 
        'year':date.year,
    }
    answer['verbose_name'] = _('{quarter} квартал {year}').format(**answer)
    return answer