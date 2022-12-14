from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    stripe.api_key = settings.STRIPE_SECRET_KEY

    @classmethod
    def create_payment_intent_sheet(cls, cus_id, cents):
        ephemeralKey = stripe.EphemeralKey.create(
            customer=cus_id,
            stripe_version=settings.STRIPE_VERSION,
        )
        paymentIntent = stripe.PaymentIntent.create(
            amount=cents,
            currency=settings.STRIPE_CURRENCY,
            customer=cus_id
        )

        return {
            "paymentIntent": paymentIntent.client_secret,
            "ephemeralKey": ephemeralKey.secret,
            "customer": cus_id
        }

    @classmethod
    def get_payments_history(cls, cus_id, limit=100, offset=0):
        return stripe.PaymentIntent.list(
            customer=cus_id, limit=limit, offset=offset,
        ).get('data', [])

    @classmethod
    def get_payments_methods(cls, cus_id, type='card', limit=100, offset=0):
        return stripe.PaymentMethod.list(customer=cus_id, type=type, limit=limit, offset=offset).get('data', [])
