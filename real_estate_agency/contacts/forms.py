from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField


class CallbackForm(forms.Form):
    name = forms.CharField(
        label=_('Имя'),
        max_length=127,
        widget=forms.TextInput(attrs={'placeholder': _('Александр')}),
    )
    phone_number = PhoneNumberField(
        label=_(''),
        widget=forms.TextInput(attrs={'placeholder': '+79995475707'}),
    )

    def is_valid(self):
        valid = super().is_valid()

        # It is necessary for inter russian calls
        # It is commonplace to call by 8 (983)... against +7 (983)...
        raw_data = self.data.get('phone_number')
        if not self.cleaned_data.get('phone_number') and raw_data[0] == '8':
                self.cleaned_data['phone_number'] = "+7" + raw_data[1:]
                if MortgageForm(self.cleaned_data).is_valid():
                    self._errors.pop('phone_number', None)
                    return True
        return valid