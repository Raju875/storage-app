from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.conf import settings

from stripe_payment.models import *
from .serializers import *
from stripe_payment.utils import *


class PaymentMethodView(ModelViewSet):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    queryset = None

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PaymentMethodDetailsSerializer
        elif self.action == 'update':
            return PaymentMethodUpdateSerializer
        return PaymentMethodSerializer

    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            raise serializers.ValidationError({'error': _('Payment method not found!.[SP-112]')})
        if obj.is_default == True:
            raise serializers.ValidationError({'error': _('Default card not remove. Change default card & try again.[SP-113]')})
        try:
            detach_payment_method(obj.payment_method_id)
            obj.delete()
            return Response({'success': _('Card remvove successfully')}, status=status.HTTP_204_NO_CONTENT)
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SP-114]')})
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[SP-115]')})


class StripePaymentView(ModelViewSet):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    http_method_names = ['post', 'put']
    queryset = None

    def get_serializer_class(self):
        if self.action == 'update':
            return StripePaymentUpdateSerializer
        return StripePaymentSerializer

    def get_queryset(self):
        return StripePayment.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super(StripePaymentView, self).create(request, *args, **kwargs)


class ApplePaySubscriptionAPI(CreateAPIView):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    queryset = StripePayment.objects.none()
    serializer_class = ApplePaySubscriptionSerializer

    def create(self, request, *args, **kwargs):
        return super(self.__class__, self).create(request, *args, **kwargs)


class ApplePayCompleteSubscriptionAPI(CreateAPIView):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    queryset = StripePayment.objects.none()
    serializer_class = ApplePayCompleteSubscriptionSerializer

    def create(self, request, *args, **kwargs):
        return super(self.__class__, self).create(request, *args, **kwargs)


class Config(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        email = request.user.email
        try:
            customer = request.user.stripe_payment
        except Exception:
            customer = app_create_stripe_customer(request.user)
        if not customer:
            raise serializers.ValidationError({'error': _('No customer found.[SP-100]')})
        try:
            publishable_key = settings.STRIPE_PUBLISHABLE_KEY
            return Response({'publishable_key': publishable_key})
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e)+'[SP-141]')})


class APIInfo(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            stripe_user = request.user.stripe_payment
            pricing_plan = retrieve_pricing_plan(settings.STRIPE_ANNUAL_PRICE_PLAN_ID)
            product = retrieve_stripe_product(pricing_plan.product)
            return Response({
                'product': {
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_description': product.description,
                    'product_image': product.images,
                    'product_price_id': pricing_plan.id,
                    'currency': pricing_plan.currency,
                    'amount': int(pricing_plan.unit_amount / 100),
                    'billing_scheme': pricing_plan.billing_scheme,
                    'recurring': pricing_plan.recurring,
                },
                'subscription': {
                    'trial_status': stripe_user.is_trial,
                    'active_status': stripe_user.is_active,
                    'cancel_status': stripe_user.is_cancel,
                    'subscription_id': stripe_user.subscription_id,
                }
            })
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[SP-142]')})


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def stripe_webhooks(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        web_secret = settings.STRIPE_WEBHOOK_SIGNING_KEY
        event = stripe.Webhook.construct_event(payload, sig_header, web_secret)
    except ValueError:
        return HttpResponse('Invalid payload![SP-171]', status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        print(e.user_message + '[SP-172]')
        return HttpResponse(_(e.user_message + '[SP-172]'), status=status.HTTP_400_BAD_REQUEST)

    # Handle the event
    if event.type == 'charge.succeeded':
        try:
            payment_intent = retrieve_payment_intent(event.data.object.payment_intent)
            if not payment_intent.customer:
                return HttpResponse('This was one time payment[SP-173]', status=status.HTTP_400_BAD_REQUEST)
            customer = retrieve_stripe_customer(payment_intent.customer)
        except StripeError as e:
            print(str(e) + '[SP-174]')
            return HttpResponse(_(e.user_message + '[SP-174]'), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e) + '[SP-175]')
            return HttpResponse(_(str(e) + '[SP-175]'), status=status.HTTP_400_BAD_REQUEST)

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(**{User.EMAIL_FIELD: customer.email})
        except Exception as e:
            print(str(e) + '[SP-176]')
            return HttpResponse(_(str(e) + '[SP-176]'), status=status.HTTP_400_BAD_REQUEST)

        try:
            stripe_customer = StripePayment.objects.get(user_id=user.id)
            subscription = retrieve_customer_subscription(stripe_customer.subscription_id)
            from django.db.models import F
            stripe_customer.no_of_subscriptions = F('no_of_subscriptions') + 1
            stripe_customer.paid_until = subscription['current_period_end']
            intent_id = latest_subscription_invoice(subscription.latest_invoice).payment_intent
            stripe_customer.payment_intent_id = intent_id
            stripe_customer.payment_intent_client_secret = retrieve_payment_intent(intent_id).client_secret
            stripe_customer.trial = False
            stripe_customer.is_cancel = False
            stripe_customer.is_active = True
            stripe_customer.save()
        except Exception as e:
            print(str(e) + '[SP-177]')
            return HttpResponse(_(str(e) + '[SP-177]'), status=status.HTTP_400_BAD_REQUEST)

    elif event.type == 'customer.subscription.created' or event.type == 'customer.subscription.updated':
        try:
            subscription = event.data.object.id
            customer = event.data.object.customer
            current_period_end = event.data.object.current_period_end
            sub = StripePayment.objects.filter(customer_id=customer, subscription_id=subscription).first()
            if sub:
                sub.paid_until = current_period_end
                sub.is_trial = False
                # sub.is_cancel = False
                # sub.is_active = True
                sub.save()
        except Exception as e:
            print(str(e) + '[SP-178]')
            return HttpResponse(_(str(e) + '[SP-178]'), status=status.HTTP_400_BAD_REQUEST)

    elif event.type == 'customer.subscription.deleted':
        try:
            subscription = event.data.object.id
            customer = event.data.object.customer
            sub = StripePayment.objects.filter(customer_id=customer, subscription_id=subscription).first()
            if sub:
                # PaymentMethod.objects.filter(customer_id=customer, payment_method_id=sub.payment_method_id).update(is_default=False)
                sub.payment_method_id = ''
                sub.subscription_id = ''
                sub.payment_intent_id = ''
                sub.payment_intent_client_secret = ''
                sub.paid_until = 0000
                sub.is_trial = False
                sub.is_cancel = True
                sub.is_active = False
                sub.save()
        except Exception as e:
            print(str(e) + '[SP-179]')
            return HttpResponse(_(str(e) + '[SP-179]'), status=status.HTTP_400_BAD_REQUEST)

    elif event.type == 'customer.deleted':
        try:
            customer_id = event.data.object.id
            stripe_cus = StripePayment.objects.filter(customer_id=customer_id).first()
            if stripe_cus:
                PaymentMethod.objects.filter(user_id=stripe_cus.user_id).delete()
                stripe_cus.delete()
        except Exception as e:
            print(str(e) + '[SP-180]')
            return HttpResponse(_(str(e) + '[SP-180]'), status=status.HTTP_400_BAD_REQUEST)

    # pending
    elif event.type == 'customer.subscription.trial_will_end':
        print('trial will end')
        pass

    return HttpResponse('Successfully received request.', status=status.HTTP_200_OK)
