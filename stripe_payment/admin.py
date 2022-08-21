from django.contrib import admin
from modules.utils import *
from .utils import retrieve_payment_method, retrieve_customer_subscription
from .models import StripePayment, PaymentMethod


@admin.register(StripePayment)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer_id', 'payment_method_id', 'subscription_id', 'paid_until', 'is_trial', 'is_active', 'is_cancel','no_of_subscriptions']
    readonly_fields = ['get_details']
    search_fields = ['customer_id', 'user__username']
    autocomplete_fields = ['user']

    def get_details(self, instance):
        if instance.subscription_id:
            subscription = retrieve_customer_subscription(instance.subscription_id)
            return json_style_prettify(subscription)
        return None

    get_details.short_description = 'Subscription'


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer', 'token_id', 'payment_method_id', 'fingerprint', 'is_default', 'is_active']
    readonly_fields = ['get_details']
    search_fields = ['payment_method_id']

    def get_details(self, instance):
        if instance.payment_method_id:
            payment_method = retrieve_payment_method(instance.payment_method_id)
            return json_style_prettify(payment_method)
        return None

    get_details.short_description = 'Payment Method'
