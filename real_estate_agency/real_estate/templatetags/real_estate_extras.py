from django import template
from django.template.defaultfilters import stringfilter
from django.template.exceptions import TemplateSyntaxError

register = template.Library()
# pluralize for russian language
# {{someval|rupluralize:"товар,товара,товаров"}}
# Idea from https://gist.github.com/xfenix/4761104
@register.filter(is_safe = False)
@stringfilter
def rupluralize(value, arg):
    bits = arg.split(u',')
    print(value)
    try:
        value = str(int(value))[-1]
        return bits[ 0 if value=='1' else (1 if value in '234' else 2) ]
    except ValueError:
        raise TemplateSyntaxError
    return ''