from decimal import Decimal

from django.shortcuts import render
from django.views.generic import FormView

from .forms import MortgageForm


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
            context['monthly_payment'] = self.calculateMortgageAnnuityPaymentForSberbank(
                price=price*(1-initial_fee),
                years=years,
            )
        return self.render_to_response(context)

    def calculateMortgageAnnuityPaymentForSberbank(self, price, years):
        lte_7years_percentage = Decimal(7.4)
        gt_7years_percentage = Decimal(9.4)
        if years <= 7:
            return self.calculateMortgageAnnuityPayment(
                price,
                years,
                lte_7years_percentage
            )
        else:
            return self.calculateMortgageAnnuityPayment(
                price,
                years,
                gt_7years_percentage
            )

    def calculateMortgageAnnuityPayment(self, price=0, years=0, percentage=Decimal(9.4)):
        from math import pow as mpow
        months = years*12
        percentage /= 1200
        return price * percentage / (1 - Decimal(mpow(1 + percentage, -months)))
