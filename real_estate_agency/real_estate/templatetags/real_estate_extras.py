import re

from django import template
from django.template.defaultfilters import stringfilter
from django.template.exceptions import TemplateSyntaxError

import pymorphy2


morph = pymorphy2.MorphAnalyzer()
morph_rgx = re.compile("(\w[\w'-]*\w|\w)")

register = template.Library()
# pluralize for russian language
# {{someval|rupluralize:"товар,товара,товаров"}}
# Idea from https://gist.github.com/xfenix/4761104

MORPHY_LINK = 'http://pymorphy2.readthedocs.io/en/latest/user/grammemes.html'


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
    for word in words:
        prefix = ''
        initial_word = word

        # For handling situations like Дизайн-квартал
        # It must change only last word, because of agreement
        # And skip TypeError at hypen
        if "-" in word:
            all_words_in_this_word = word.split('-')
            word = all_words_in_this_word.pop()
            prefix = '-'.join(all_words_in_this_word) + "-"
            prefix = prefix.lower()

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
            try:
                cased_words = parsed.inflect({case})
            except ValueError:
                # a = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct']
                raise TemplateSyntaxError(
                    'Unknown case "%s", see known at %s' % (case, MORPHY_LINK))

            if cased_words:
                cased_word = prefix + cased_words[0]
                output_value = output_value.replace(initial_word, cased_word)
    return output_value


@register.simple_tag
def extra_head(template_name='base/extra_head.html'):
    try:
        return template.loader.get_template(template_name).render()
    except template.TemplateDoesNotExist:
        return ""
