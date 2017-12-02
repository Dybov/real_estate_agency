import decimal

from django.shortcuts import render
from django.views.generic import FormView

from .forms import MortgageForm

def _index(request):
    context = {'form':MortgageForm}
    return render(request, 'mortgage/calculator.html', context)

class index(FormView):
    form_class = MortgageForm
    template_name = 'mortgage/calculator.html'
    success_url = '...'
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.GET or None)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        if form.is_valid():
            price = form.cleaned_data['full_price']
            initial_fee = form.cleaned_data['initial_fee_percentage']/100
            years = form.cleaned_data['years']
            context['monthly_payment'] = self.calculateMortgageAnnuityPayment(
                price=price*(1-initial_fee),
                years=years,
            )
        return self.render_to_response(context)

    def calculateMortgageAnnuityPayment(
            self,
            price=0,
            years=0,
            percentage=decimal.Decimal(9.4)
            ):
        from math import pow as mpow
        months = years*12
        percentage/=1200
        return price * percentage / (1- decimal.Decimal(mpow(1 + percentage, -months)))
