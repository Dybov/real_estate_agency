from django.shortcuts import render
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import telepot

from .forms import CallbackForm
from .models import CallbackRequest


TOKEN = settings.TELEGRAM_TOKEN
TelegramBot = telepot.Bot(TOKEN)
MSG_RECEIVERS = settings.TELEGRAM_CHATS


DEFAULT_TELEGRAM_MESSAGE = _('''Поступила заявка:
Имя: %(name)s
Телефон: %(phone)s

Источник: %(url)s
''')


class Callback(FormView):
    template_name = 'applications/callback.html'  # 'contacts/callback.html'
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
        # Save model with all params
        self.saveModel(form)
        # Send messages to list of interested_persons
        self.sendCallbackRequestToTelegram(form, TelegramBot, MSG_RECEIVERS)
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

    def sendCallbackRequestToTelegram(self, form, bot, receivers=[]):
        msg = DEFAULT_TELEGRAM_MESSAGE % {'name': form.cleaned_data.get('name'),
                                          'phone': form.cleaned_data.get('phone_number'),
                                          'url': self.request.META.get('HTTP_REFERER'),
                                          }
        extra_field = form.cleaned_data.get('extra_info')
        if extra_field and extra_field!='None':
            msg += _('\nДополнительная информация: %(extra)s') % {
                'extra': extra_field}
        for chat_id in receivers:
            try:
                bot.sendMessage(chat_id, msg)
            except TelegramError:
                import logging
                # Get an instance of a logger
                logger = logging.getLogger(__name__)
                logger.critical('Bad telegram token is set %s' % TOKEN)
            except:
                pass

    def saveModel(self, form):
        data = form.cleaned_data
        data.update({'url_from':self.request.META.get('HTTP_REFERER')})
        obj = CallbackRequest(**data)
        obj.save()
        return obj