from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField


class RussianPhoneNumberFormMixin(object):
    PHONE_NUMBER_FIELD = 'phone_number'
    def is_valid(self, *args, **kwargs):
        valid = super(RussianPhoneNumberFormMixin, self).is_valid()

        # It is necessary for inter russian calls
        raw_data = self.data.get(self.PHONE_NUMBER_FIELD)
        if not self.cleaned_data.get(self.PHONE_NUMBER_FIELD):
            transformed8 = transform_russian8_phone_number(raw_data)
            if transformed8!=raw_data:
                self.cleaned_data[self.PHONE_NUMBER_FIELD] = transformed8
                self._errors.pop(self.PHONE_NUMBER_FIELD, None)
                valid = super(RussianPhoneNumberFormMixin, self).is_valid()
        return valid



class CallbackForm(RussianPhoneNumberFormMixin, forms.Form):
    name = forms.CharField(
        label=_('Имя'),
        max_length=127,
        widget=forms.TextInput(attrs={'placeholder': _('Владимир')}),
        required=False,
    )
    phone_number = PhoneNumberField(
        label=_('Номер телефона'),
        widget=forms.TextInput(attrs={'placeholder': '+79995475707'}),
    )
    extra_info = forms.CharField(widget = forms.HiddenInput(), required = False)


def transform_russian8_phone_number(phone_number):
    # It is commonplace to call by 8 (983)... against +7 (983)...
    if phone_number and phone_number[0]=='8':
        phone_number = '+7' + phone_number[1:]
    return phone_number