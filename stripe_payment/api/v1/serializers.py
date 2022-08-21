from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from stripe.error import StripeError

from stripe_payment.models import *
from stripe_payment.utils import *


class PaymentMethodSerializer(serializers.ModelSerializer):
    number = serializers.CharField(write_only=True, required=True)
    exp_month = serializers.IntegerField(write_only=True, required=True)
    exp_year = serializers.IntegerField(write_only=True, required=True)
    cvc = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = PaymentMethod
        fields = ['number', 'exp_month', 'exp_year', 'cvc', 'user', 'customer', 'payment_method_id', 'is_default']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'customer': {
                'read_only': True
            },
            'payment_method_id': {
                'read_only': True
            },
            'is_default': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        request_user = self.context['request'].user
        data = validated_data
        try:
            customer = request_user.stripe_payment
        except Exception as e:
            customer = app_create_stripe_customer(request_user)
        if not customer:
            raise serializers.ValidationError({'error': _('Payment method create failed for this customer.[SP-101]')})
        try:
            card_token = create_card_token(data)
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SP-102]')})

        check_exists = PaymentMethod.objects.filter(customer=customer, fingerprint=card_token.card.fingerprint)
        if check_exists.exists():
            raise serializers.ValidationError({'error': _('You already have this card saved.[SP-103]')})
        try:
            payment_method = create_payment_method(data, request_user)
            attach_payment_method(payment_method.id, customer.customer_id)
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SP-104]')})
        except Exception as e:
            raise serializers.ValidationError({'error': _('Failed to create payment method.[SP-105]')})
        return PaymentMethod.objects.create(user=request_user,
                                            customer=request_user.stripe_payment,
                                            token_id=card_token.id,
                                            payment_method_id=payment_method.id,
                                            fingerprint=card_token.card.fingerprint,
                                            is_default=False)


class PaymentMethodDetailsSerializer(serializers.ModelSerializer):
    api_details = serializers.JSONField(read_only=True)

    class Meta:
        model = PaymentMethod
        fields = ['id', 'user', 'customer', 'payment_method_id', 'is_default', 'created_at', 'api_details']


class PaymentMethodUpdateSerializer(serializers.ModelSerializer):
    exp_month = serializers.IntegerField(write_only=True, required=True)
    exp_year = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = PaymentMethod
        fields = ['exp_month', 'exp_year', 'payment_method_id']

    def update(self, instance, validated_data):
        card_token = retrieve_card_token(instance.token_id)
        if not card_token:
            raise serializers.ValidationError({'error': _('Invalida token![SP-106]')})
        try:
            modify_payment_method(instance.payment_method_id, validated_data)
            return instance
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SP-107]')})
        except Exception as e:
            raise serializers.ValidationError({'error': _('Failed to update payment method.[SP-108]')})


class StripePaymentSerializer(serializers.ModelSerializer):
    payment_method_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = StripePayment

        fields = ['user', 'subscription_id', 'payment_method_id']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'subscription_id': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        request_user = self.context['request'].user
        payment_method_id = validated_data.pop('payment_method_id')
        try:
            customer = request_user.stripe_payment
            customer_id = customer.customer_id
        except StripePayment.DoesNotExist:
            customer = app_create_stripe_customer(request_user)
            customer_id = customer.customer_id

        if not customer_id:
            raise serializers.ValidationError({'error': _('No customer found.[SP-116]')})

        check_exists = PaymentMethod.objects.filter(customer=customer, payment_method_id=payment_method_id)
        if not check_exists.exists():
            raise serializers.ValidationError({'error': _('Invalid payment method.[SP-118]')})
        try:
            pricing_plan = retrieve_pricing_plan(settings.STRIPE_ANNUAL_PRICE_PLAN_ID)
            customer_default_payment_method(customer_id, payment_method_id)
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SP-119]')})
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[SP-120]')})
        
        subscription = None
        if customer.is_active:
            raise serializers.ValidationError({'error': _('Already have active subscription.Cancel it first & try again.[SP-117]')})
        try:
            if customer.is_trial:
                trial_days = pricing_plan.recurring.trial_period_days
                subscription = create_trial_subscription(customer_id, pricing_plan.id, trial_days)
            else:
                payment_settings = {'save_default_payment_method': 'on_subscription'}
                expand = ['latest_invoice.payment_intent']
                subscription = create_stripe_subscription(customer_id, payment_method_id, pricing_plan.id, payment_settings, expand)
                intent_id = latest_subscription_invoice(subscription.latest_invoice.id).payment_intent
                customer.payment_intent_id = intent_id
                customer.payment_intent_client_secret = retrieve_payment_intent(intent_id).client_secret

            if subscription:
                customer.payment_method_id = payment_method_id
                customer.subscription_id = subscription.id
                customer.is_trial = False
                customer.is_active = True
                customer.is_cancel = False
                customer.save()

                payment_method = PaymentMethod.objects.filter(customer=customer)
                payment_method.update(is_default=False)
                payment_method.filter(payment_method_id=payment_method_id).update(is_default=True)

            return customer
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SP-121]')})
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[SP-122]')})


class StripePaymentUpdateSerializer(serializers.ModelSerializer):
    is_cancel = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = StripePayment
        fields = ['user', 'subscription_id', 'is_cancel', 'is_active']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'subscription_id': {
                'read_only': True
            },
            'is_active': {
                'read_only': True
            }
        }

    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        is_cancel = validated_data.pop('is_cancel')
        try:
            customer = request_user.stripe_payment
        except StripePayment.DoesNotExist:
            raise serializers.ValidationError({'error': _('No customer found.[SP-151]')})
        if customer.is_active == False:
            raise serializers.ValidationError({'error': _('No active subscription found.[SP-152]')})
        try:
            if is_cancel == True:
                cancel_stripe_subscription(customer.subscription_id)
                customer.is_cancel = True
            else:
                not_cancel_stripe_subscription(customer.subscription_id)
                customer.is_cancel = False
            customer.save()
            return customer
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SP-153]')})
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[SP-154]')})


class ApplePaySubscriptionSerializer(serializers.ModelSerializer):
    payment_method_id = serializers.CharField(write_only=True, required=True)
    payment_intent_id = serializers.CharField(read_only=True)
    payment_intent_client_secret = serializers.CharField(read_only=True)

    class Meta:
        model = StripePayment

        fields = ['user','subscription_id','payment_method_id','payment_intent_id','payment_intent_client_secret','is_active']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'subscription_id': {
                'read_only': True
            },
            'is_active': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        request_user = self.context['request'].user
        customer_id = None
        payment_method_id = validated_data.pop('payment_method_id')
        try:
            customer = request_user.stripe_payment
            customer_id = customer.customer_id
        except StripePayment.DoesNotExist:
            customer = app_create_stripe_customer(request_user)
            customer_id = customer.customer_id

        if not customer_id:
            raise serializers.ValidationError({'error': _('No customer found.[SAP-101]')})
            
        try:
            pricing_plan = retrieve_pricing_plan(settings.STRIPE_ANNUAL_PRICE_PLAN_ID)
            fingerprint = retrieve_payment_method(payment_method_id).card.fingerprint
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SAP-102]')})
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[SAP-103]')})

        check_exists = PaymentMethod.objects.filter(customer=customer, fingerprint=fingerprint)
        if not check_exists.exists():
            try:
                attach_payment_method(payment_method_id, customer_id)
                PaymentMethod.objects.create(user=request_user,
                                            customer=customer,
                                            token_id='apple-pay-token',
                                            payment_method_id=payment_method_id,
                                            fingerprint=fingerprint,
                                            is_default=False)
                customer_default_payment_method(customer_id, payment_method_id)
            except StripeError as e:
                raise serializers.ValidationError({'error': _(e.user_message + '[SAP-104]')})
            except Exception as e:
                raise serializers.ValidationError({'error': _(str(e) + '[SAP-105]')})

        if customer.is_active:
            raise serializers.ValidationError({'error': _('Already have active subscription.Cancel it first & try again.[SAP-106]')})
        try:
            subscription = None
            if customer.is_trial:
                trial_days = pricing_plan.recurring.trial_period_days
                subscription = create_trial_subscription(customer_id, pricing_plan.id, trial_days)

                payment_intent_id = subscription.pending_setup_intent
                payment_intent_client_secret = retrieve_setup_payment_intent(payment_intent_id).client_secret
                customer.is_trial = False
                customer.is_active = True
            else:
                payment_behavior = 'default_incomplete'
                # payment_behavior = 'allow_incomplete'
                payment_settings = {'save_default_payment_method': 'on_subscription'}
                expand = ['latest_invoice.payment_intent']
                subscription = create_incomplete_stripe_subscription(customer_id=customer_id, payment_method_id=payment_method_id, pricing_plan_id=pricing_plan.id,
                                                                     payment_behavior=payment_behavior,
                                                                     payment_settings=payment_settings,
                                                                     expand=expand)

                payment_intent_id = latest_subscription_invoice(subscription.latest_invoice.id).payment_intent
                payment_intent_client_secret = retrieve_payment_intent(payment_intent_id).client_secret
                customer.is_active = False

            if subscription:
                customer.payment_method_id = payment_method_id
                customer.subscription_id = subscription.id
                customer.payment_intent_id = payment_intent_id
                customer.payment_intent_client_secret = payment_intent_client_secret
                customer.is_cancel = False
                customer.save()

                payment_method = PaymentMethod.objects.filter(customer=customer)
                payment_method.update(is_default=False)
                payment_method.filter(payment_method_id=payment_method_id).update(is_default=True)
            
            return customer
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SAP-107]')})
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[SAP-108]')})


class ApplePayCompleteSubscriptionSerializer(serializers.ModelSerializer):
    payment_intent_id = serializers.CharField(write_only=True, required=True)
    payment_intent_client_secret = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = StripePayment

        fields = ['user','subscription_id','payment_method_id','payment_intent_id','payment_intent_client_secret','is_trial','is_active']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'subscription_id': {
                'read_only': True
            },
            'payment_method_id': {
                'read_only': True
            },
            'is_trial': {
                'read_only': True
            },
            'is_active': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        request_user = self.context['request'].user
        payment_intent_id = validated_data.pop('payment_intent_id')
        payment_intent_client_secret = validated_data.pop('payment_intent_client_secret')
        try:
            customer = request_user.stripe_payment
        except StripePayment.DoesNotExist:
            raise serializers.ValidationError({'error': _('No customer found.[SAP-161]')})

        if customer.is_active:
            raise serializers.ValidationError({'error': _('Already have active subscription.Cancel it first & try again.[SAP-162]')})

        if customer.payment_intent_id != payment_intent_id or customer.payment_intent_client_secret != payment_intent_client_secret:
            raise serializers.ValidationError({'error': _('Invalid data. Try again.[SAP-163]')})
        
        customer.is_trial = False
        customer.is_active = True
        customer.is_cancel = False
        customer.save()

        return customer
