from django.views.generic import FormView
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse

from .forms import CallbackForm
from .models import CallbackRequest
from .middleware import UTM_PARAMS
from .sendmail_helper import sendMailToTheManagers
from .viber_tasks import sendViberTextMessageToTheAdmins

DEFAULT_MSG_TITLE = _("Заявка с сайта %(domain)s")
DEFAULT_DOMAIN = None
DEFAULT_MESSAGE = _('''<b>Поступила заявка:</b>
Имя: %(name)s
Телефон: %(phone)s

Источник: %(url)s''')

if settings.DEBUG:
    DEFAULT_MESSAGE = "%s%s" % (
        _('<h1>[DEBUG MODE]</h1>\n\n'),
        DEFAULT_MESSAGE
    )

EXTRA_MESSAGE = _('\n\n<b>Дополнительная информация:</b> %(extra)s\n\n')
MARKETING_MESSAGE = _('''\n<b>Рекламная кампания:</b>
UTM source: %(utm_source)s
UTM medium: %(utm_medium)s
UTM campaign: %(utm_campaign)s
UTM content: %(utm_content)s
UTM term: %(utm_term)s
''')


def get_msg_title(request):
    global DEFAULT_DOMAIN, DEFAULT_MSG_TITLE
    if not DEFAULT_DOMAIN:
        from django.contrib.sites.shortcuts import get_current_site
        DEFAULT_DOMAIN = get_current_site(request).domain
    return DEFAULT_MSG_TITLE % {'domain': DEFAULT_DOMAIN}


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
        self.sendCallbackRequest(form)
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

    def sendCallbackRequest(self, form):
        msg = DEFAULT_MESSAGE % {
            'name': form.cleaned_data.get('name'),
            'phone': form.cleaned_data.get('phone_number'),
            'url': self.request.META.get('HTTP_REFERER'),
        }
        extra_field = form.cleaned_data.get('extra_info')
        if extra_field and extra_field != 'None':
            msg += EXTRA_MESSAGE % {
                'extra': extra_field}
        msg = self.addMarketingInfoToMessage(msg)
        title = get_msg_title(self.request)

        sendMailToTheManagers(title=title, message=msg)
        sendViberTextMessageToTheAdmins(msg)

    def addMarketingInfoToMessage(self, text):
        if UTM_PARAMS[0] in self.request.COOKIES:
            text += MARKETING_MESSAGE % {
                utm_name: self.request.COOKIES.get(utm_name, '-')
                for utm_name in UTM_PARAMS
            }
        return text

    def saveModel(self, form):
        data = form.cleaned_data
        data.update({'url_from': self.request.META.get('HTTP_REFERER')})
        obj = CallbackRequest(**data)
        obj.save()
        return obj
