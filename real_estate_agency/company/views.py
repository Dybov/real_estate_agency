from django.shortcuts import render
from django.template import RequestContext

from new_buildings.models import Builder, ResidentalComplex, NewApartment


# Temporary dict for bank partners
# 'Bank Name' : 'Image filewithout extension placed in static/img/partners/bank' 
BANK_PARTNERS = {
    'ПАО «Сбербанк России»' : 'sberbank',
    'ВТБ 24 (ПАО)' : 'vtb24',
    'ПАО «Запсибкомбанк»' : 'zpsib',
    'АКБ «Абсолют Банк»' : 'absolut',
    'ПАО «ТРАНСКАПИТАЛБАНК»' : 'transkapital',
    'АО «КБ ДельтаКредит»' : 'deltacredit',
    'Банк УРАЛСИБ' : 'norooturalsib',
    '«АК БАРС» Банк' : 'akbars',
    'ПАО Банк «ФК Открытие»' : 'otkretie',
    'АО «Россельхозбанк»' : 'rosselhoz',
}

def about(request):
    return render(request,
                  'company/about_company.html',
                  )
