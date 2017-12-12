from django.shortcuts import render
from django.template import RequestContext

from .forms import CallbackForm

def default_contacts_processor(request):
    "A context processor that provides contacts such as number, email, social_network_links..."
    return {
        'global_phone_number': '+7 (3452) 589-881',
        'global_chat': {
            'vk':'https://vk.com/im?media=&sel=-146199351',
            'facebook':'https://facebook/chat',
            'telegram':'https://telegram/feed',
            },
        'global_social_links': {
            'vk':'https://vk.com/domus_72',
            'instagram':'https://www.instagram.com/domus_72/',
            },
        'global_email': 'domus72@bk.ru',
        'callback_form': CallbackForm(),
        }