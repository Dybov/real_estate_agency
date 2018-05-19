from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from real_estate.models import Apartment, BaseBuilding
from new_buildings.models import ResidentalComplex


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
    residental_complex = models.ForeignKey(ResidentalComplex,
                                           verbose_name=_('Жилой комплекс'),
                                           on_delete=models.SET_DEFAULT,
                                           default=None,
                                           blank=True,
                                           null=True,
                                           )
    def clean(self):
        # Don't allow set agency_price lower than real price.
        if self.agency_price is not None and self.price is not None and self.agency_price < self.price:
            raise ValidationError({'agency_price':
                                   _('цена с комиссией от агенства %(agency_price)s должна быть больше реальной цены %(real_price)s')
                                   % {'agency_price': self.agency_price, 'real_price': self.price}
                                   })
    @property
    def fee(self):
        if self.agency_price and self.price:
            return self.agency_price - self.price

    def __str__(self):
        return self.pk
    
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

-Список состояний сделки должен быть представлен следующими значениями:
сделка активна
продано с помощью «DОМУС»
продано без участия «DОМУС»'''


