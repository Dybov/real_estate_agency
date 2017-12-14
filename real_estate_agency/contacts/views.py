from django.shortcuts import render
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

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

def index(request):
    return render(request, 'contacts/index.html')


class Callback(FormView):
    template_name = 'contacts/callback.html' #'contacts/callback.html'
    form_class = CallbackForm
    success_url = reverse_lazy('thanks')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.items(), status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {}
            return JsonResponse(data)
        else:
            return response
    

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # override standart callback_form (from context processor)
        data['callback_form'] = data.get('form')
        return data
