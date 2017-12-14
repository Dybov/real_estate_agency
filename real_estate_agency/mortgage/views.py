from decimal import Decimal

from django.shortcuts import render
from django.views.generic import FormView

from .forms import MortgageForm


class Index(FormView):
    form_class = MortgageForm
    template_name = 'mortgage/calculator.html'
    success_url = '...'
    initial = {'full_price': 1200000,
               'initial_fee': int(1200000*0.2),
               'years': 15,
               }

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.GET or self.get_initial())
        context = self.get_context_data(**kwargs)
        context['form'] = form
        if form.is_valid():
            price = form.cleaned_data['full_price']
            initial_fee = form.cleaned_data['initial_fee']
            years = form.cleaned_data['years']

            calc_results = self.calculateMortgageAnnuityPaymentForSberbank(
                full_price=price,
                years=years,
                initial_fee=initial_fee,
            )
            context.update(calc_results)
        return self.render_to_response(context)
    
    def calculateMortgageAnnuityPaymentForSberbank(self, full_price, years, initial_fee):
        output_params = {'full_price': full_price,
                         'years': years,
                         'initial_fee': initial_fee,
                         }
        if years <= 7:
            output_params['mortgage_percentage'] = Decimal(7.4)
        elif years <= 12:
            output_params['mortgage_percentage'] = Decimal(7.9)
        return self.calculateMortgageAnnuityPayment(**output_params)

    def calculateMortgageAnnuityPayment(self, full_price=0, years=0, initial_fee=0, mortgage_percentage=Decimal(9.4)):
        from math import pow as mpow
        price = full_price - initial_fee
        months = years*12
        monthly_mortgage_proportion = mortgage_percentage / 1200
        monthly_payment = price * monthly_mortgage_proportion / \
            (1 - Decimal(mpow(1 + monthly_mortgage_proportion, -months)))
        return {'monthly_payment': monthly_payment,
                'mortgage_percentage': mortgage_percentage,
                'amount_of_mortgage': price,
                }
