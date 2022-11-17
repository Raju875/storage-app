from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.auth import get_user_model
from stripe_payment.utils import *

User = get_user_model()


class PaymentMethod(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='payment_method')
    customer = models.ForeignKey('stripe_payment.StripePayment', on_delete=models.SET_NULL,null=True, blank=True, related_name='payment_method')
    token_id = models.CharField(_('Token ID'), max_length=255, blank=True, null=True)
    payment_method_id = models.CharField(_('Payment method id'), max_length=120, blank=True, null=True)
    fingerprint = models.CharField(_('Fingerprint'), max_length=120, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.payment_method_id)

    class Meta:
        verbose_name = _('Payment Method')
        verbose_name_plural = _('Payment Methods')
        ordering = ['-id']


class StripePayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stripe_payment')
    customer_id = models.CharField(_('Customer id'), max_length=200)
    payment_method_id = models.CharField(_('Payment Method id'), max_length=200, null=True, blank=True)
    subscription_id = models.CharField(_('Subscription id'), max_length=200, null=True, blank=True)
    payment_intent_id = models.CharField(_('Payment intent id'), max_length=200, null=True, blank=True)
    payment_intent_client_secret = models.CharField(_('Payment intent cliend secret'), max_length=200, null=True, blank=True)
    paid_until = models.CharField(_("Paid until"), max_length=200, null=True, blank=True)
    no_of_subscriptions = models.IntegerField(_("No of subscription"), default=0)
    is_trial = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.customer_id)

    class Meta:
        verbose_name = _('Stripe Payment')
        verbose_name_plural = _('Stripe Payments')
        ordering = ['-id']
