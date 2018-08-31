import re

from django.conf import settings
from django.shortcuts import render

from applications.forms import CallbackForm

_phone_pattern = re.compile(
    '^(\+7|8)(9\d{2}|\d{4})(\d{2}|\d{3})(\d{2})(\d{2})$')
_phone_stringified = '%s (%s) %s-%s-%s'


DEFAULT_PHONE = getattr(settings, 'DEFAULT_PHONE', '+73452589881')
DEFAULT_EMAIL = getattr(settings, 'DEFAULT_EMAIL', 'domus72@bk.ru')
DEFAULT_CHATS = getattr(settings, 'DEFAULT_CHATS', {
    'vk': 'https://vk.com/im?media=&sel=-146199351',
    'facebook': 'https://www.facebook.com/messages/t/100013569948296',
    'telegram': 'https://t.me/Igor_Zadachin',
})
DEFAULT_SOCIAL = getattr(settings, 'DEFAULT_SOCIAL', {
    'vk': 'https://vk.com/domus_72',
    'instagram': 'https://www.instagram.com/domus_72/',
})


def phone_stringify(phone_number):
    m = _phone_pattern.search(str(phone_number))
    new_phone = phone_number
    if m:
        groups = m.groups()
        country, city, a, b, c = groups
        if len(city) + len(a) == 6:
            new_phone = _phone_stringified % groups
    return new_phone


def default_contacts_processor(request):
    """A context processor that provides contacts
    such as number, email, social_network_links..."""
    return {
        'global_phone_number_orig': DEFAULT_PHONE,
        'global_phone_number': phone_stringify(DEFAULT_PHONE),
        'global_chat': DEFAULT_CHATS,
        'global_social_links': DEFAULT_SOCIAL,
        'global_email': DEFAULT_EMAIL,
        'callback_form': CallbackForm(),
    }


def index(request):
    return render(request, 'contacts/index.html')
