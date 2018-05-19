from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from real_estate.models import Apartment, BaseBuilding


class ResaleApartment(Apartment, BaseBuilding):
    agency_price = models.DecimalField(verbose_name=_('цена с комиссией от агенства, рб'),
                                       default=1000000,
                                       decimal_places=0,
                                       max_digits=15,
                                       validators=[MinValueValidator(
                                                   Decimal('0.0')
                                                   ),
                                                   ],
                                       )

    def clean(self):
        # Don't allow set agency_price lower than real price.
        if self.agency_price is not None and self.price is not None and self.agency_price < self.price:
            raise ValidationError({'agency_price':
                _('цена с комиссией от агенства %(agency_price)s должна быть больше реальной цены %(real_price)s')
                % {'agency_price': self.agency_price, 'real_price': self.price}
                })

    class Meta:
        verbose_name = _('объект вторичка')
        verbose_name_plural = _('вторички')


'''
Ко вторичному жилью относятся квартиры. Квартира должна иметь следующие поля:
+ количество комнат (список количества комнат)
+ цена  от продавца (вещественное число) просто цена
+\ цена с комиссией от агенства (вещественное число) f?
+ описание (текст)
+ отображать во вторичках (флаг)
//Отдельная абстрактная модель
+ район (список районов)
+ улица (список улиц)
+ дом (целое число)
+ корпус (строка)
+ исполнение дома (список возможных исполнений дома)
+ количество этажей (целое число)
+ жилой комплекс (список жилых комплексов)
//
+ планировка (изображение)
+ общая площадь (вещественное число)
+ площадь кухни (вещественное число)
+ площадь балкона (вещественное число)
+ вид отделки (список видов отделки)
+ высота потолка (вещественное число)
+ этаж (строка)
- сделка (связанный объект)
- Сделка должна иметь следующие поля:
- состояние сделки (список состояний сделки)
- комментарий (текст)
?- риэлтор (автоматичеси заполняемое поле — пользователь создавший сделку)
- комиссия (автоматичеси вычисляемое поле — разница между ценой от продавца и ценой от агенства)
- объект сделки (связанная квартира)

Список количества комнат должен представлять собой следующие значения:
Студия
1
2
3
4
5
6
7

+Список районов и список улиц должны представлять собой динамически создаваемые списки, которые зависят от заполнения соответствующих полей в разделе «адрес» в админке.
+Список возможных исполнений дома должен быть представлен следующими значениями:
кирпичный
монолитный
каркасный
панельный
монолитно-каркасный
панельный-кирпичный
блоки железобетоные
cиликатный блок

+Список видов отделки должен быть представлен следующими значениями:
ремонт
евро ремонт
чистовая
предчистовая
улучшенная черновая
черновая

+Список жилых комплексов должен представлять собой динамически создаваемый список, который зависит от заполнения соответствующих полей в разделе «новостройки» в админке.
-Список состояний сделки должен быть представлен следующими значениями:
сделка активна
продано с помощью «DОМУС»
продано без участия «DОМУС»'''


'''
class LastUserField(models.ForeignKey):
    """
    A field that keeps the last user that saved an instance
    of a model. None will be the value for AnonymousUser.
    """

    def __init__(self, to=getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), on_delete=models.SET_NULL, null=True, editable=False,  **kwargs):
        super(LastUserField, self).__init__(to=to, on_delete=on_delete, null=null, editable=editable, **kwargs)

    def contribute_to_class(self, cls, name):
        super(LastUserField, self).contribute_to_class(cls, name)
        registry = registration.FieldRegistry(self.__class__)
registry.add_field(cls, self)
'''
