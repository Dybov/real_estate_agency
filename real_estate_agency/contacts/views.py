from django.shortcuts import render


from applications.forms import CallbackForm

def default_contacts_processor(request):
    """A context processor that provides contacts 
    such as number, email, social_network_links..."""
    return {
        'global_phone_number': '+7 (3452) 58-98-81',
        'global_chat': {
            'vk': 'https://vk.com/im?media=&sel=-146199351',
            'facebook': 'https://www.facebook.com/messages/t/100013569948296',
            'telegram': 'https://t.me/Igor_Zadachin',
        },
        'global_social_links': {
            'vk': 'https://vk.com/domus_72',
            'instagram': 'https://www.instagram.com/domus_72/',
        },
        'global_email': 'domus72@bk.ru',
        'callback_form': CallbackForm(),
    }


def index(request):
    return render(request, 'contacts/index.html')
