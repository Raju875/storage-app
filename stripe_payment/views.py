from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class GooglePayTestView(LoginRequiredMixin, TemplateView):
    template_name = 'stripe_payment/google_pay_test.html'

    def get_context_data(self, **kwargs):
        ctx = super(self.__class__, self).get_context_data(**kwargs)
        ctx['publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        # try:
        #     ctx['cart'] = self.request.user.cart_user.get(cart_status='active')
        # except:
        #     ctx['cart'] = None
        return ctx
