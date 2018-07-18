import re

from django import template
from django.template.defaultfilters import stringfilter
from django.template.exceptions import TemplateSyntaxError

import pymorphy2


morph = pymorphy2.MorphAnalyzer()
morph_rgx = re.compile("(\w[\w']*\w|\w)")

register = template.Library()
# pluralize for russian language
# {{someval|rupluralize:"товар,товара,товаров"}}
# Idea from https://gist.github.com/xfenix/4761104


@register.filter(is_safe=False)
@stringfilter
def rupluralize(value, arg):
    bits = arg.split(u',')
    try:
        value = str(int(value))[-1]
        return bits[0 if value == '1' else (1 if value in '234' else 2)]
    except ValueError:
        raise TemplateSyntaxError
    return ''


@register.filter(is_safe=False)
@stringfilter
def morphy_by_case(value, case):
    output_value = value
    words = morph_rgx.split(value)
    try:
        for word in words:
            if re.findall('(ой$)', word, re.I | re.U):
                for pars in morph.parse(word):
                    if "ADJF" in pars.tag:
                        parsed = pars
                        break
            else:
                parsed = morph.parse(word)
                if parsed:
                    parsed = parsed[0]
            if parsed and not {'UNKN'} in parsed.tag:
                cased_word = parsed.inflect({case})[0]
                output_value = output_value.replace(word, cased_word)
    except TypeError:
        raise TemplateSyntaxError(
            'Supported only russian morphy, used "%s"' % value)
    except ValueError:
        # a = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct']
        morphy_link = \
            'http://pymorphy2.readthedocs.io/en/latest/user/grammemes.html'
        raise TemplateSyntaxError(
            'Unknown case "%s", see known at %s' % (case, morphy_link))
    except Exception:
        raise TemplateSyntaxError('Unknown error')
    return output_value


@register.simple_tag
def extra_head(template_name='base/extra_head.html'):
    try:
        return template.loader.get_template(template_name).render()
    except template.TemplateDoesNotExist:
        return ""
