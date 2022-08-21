from django.conf import settings
import stripe
from stripe.error import StripeError

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_customer(user):
    return stripe.Customer.create(
        name=user.username,
        email=user.email,
        metadata={
            'user_id': user.id
        }
    )


def app_create_stripe_customer(user):
    from .models import StripePayment
    try:
        stripe_customer = create_stripe_customer(user)
    except StripeError as err:
        print(err)
        return None
    if stripe_customer:
        from django.utils import timezone
        extend_time = timezone.now()
        return StripePayment.objects.create(user=user,
                                            customer_id=stripe_customer.id,
                                            paid_until=round(extend_time.timestamp()),
                                            is_trial=True,
                                            is_active=False,
                                            is_cancel=False)
    return None


def stripe_customer_delete(customer_id, user_id=None):
    return stripe.Customer.delete(customer_id)


def retrieve_stripe_customer(customer_id):
    return stripe.Customer.retrieve(customer_id)


def customer_default_payment_method(customer_id, payment_method_id):
    return stripe.Customer.modify(customer_id,
                                  invoice_settings={
                                      'default_payment_method': payment_method_id
                                  })


def create_card_token(data):
    return stripe.Token.create(
        card={
            "number": data['number'],
            "exp_month": data['exp_month'],
            "exp_year": data['exp_year'],
            "cvc": data['cvc']
        }
    )


def retrieve_card_token(token):
    return stripe.Token.retrieve(token)


def retrieve_stripe_product(product_id):
    return stripe.Product.retrieve(product_id)


def retrieve_pricing_plan(id):
    return stripe.Price.retrieve(id)


def create_payment_intent(data, email, customer_id, payment_method_id):
    return stripe.PaymentIntent.create(
        customer=customer_id,
        amount=data.unit_amount,
        currency=data.currency,
        payment_method_types=["card"],
        payment_method=payment_method_id,
        receipt_email=email,
        capture_method="automatic",
    )


def retrieve_payment_intent(payment_intent_id):
    return stripe.PaymentIntent.retrieve(payment_intent_id)


def modify_payment_intent(payment_intent_id, payment_method_id, customer_id):
    return stripe.PaymentIntent.modify(payment_intent_id,
                                       payment_mehthod_id=payment_method_id,
                                       customer=customer_id
                                       )


def confirm_payment_intent(intent_id):
    return stripe.PaymentIntent.confirm(intent_id)


def retrieve_setup_payment_intent(setup_intent_id):
    return stripe.SetupIntent.retrieve(setup_intent_id)



def create_payment_method(data, user):
    return stripe.PaymentMethod.create(
        type="card",
        card={
            "number": data['number'],
            "exp_month": data['exp_month'],
            "exp_year": data['exp_year'],
            "cvc": data['cvc'],
        },
        billing_details={
            'email': user.email,
            'name': user.username,
        }
    )


def retrieve_payment_method(payment_method_id):
    return stripe.PaymentMethod.retrieve(payment_method_id)


def modify_payment_method(payment_method_id, data):
    return stripe.PaymentMethod.modify(
        payment_method_id,
        card={
            "exp_month": data['exp_month'],
            "exp_year": data['exp_year']
        },
    )


def attach_payment_method(payment_method_id, customer_id):
    return stripe.PaymentMethod.attach(payment_method_id,
                                       customer=customer_id,
                                       )


def detach_payment_method(payment_method_id):
    return stripe.PaymentMethod.detach(payment_method_id)


def create_trial_subscription(customer_id, price_id, trial_days):
    if trial_days is None:
        trial_days = 7  # default 7 days
    from django.utils.timezone import timedelta
    import datetime
    trial_end = datetime.datetime.now() + timedelta(days=trial_days)

    return stripe.Subscription.create(customer=customer_id,
                                      items=[{
                                          'price': price_id
                                      }],
                                      trial_end=trial_end,
                                      payment_behavior='default_incomplete',
                                      # default_payment_method=NULL,
                                    )


def create_stripe_subscription(customer_id, payment_method_id, pricing_plan_id,
                               payment_settings, expand={}):
    return stripe.Subscription.create(customer=customer_id,
                                      items=[{
                                           'price': pricing_plan_id
                                      }],
                                      default_payment_method=payment_method_id,
                                      # trial_end='now',
                                      payment_settings=payment_settings,
                                      expand=expand
                                    )


def create_incomplete_stripe_subscription(customer_id, payment_method_id, pricing_plan_id,
                                          payment_settings,
                                          payment_behavior='default_incomplete', expand={}):
    return stripe.Subscription.create(customer=customer_id,
                                      items=[{
                                          'price': pricing_plan_id
                                      }],
                                      default_payment_method=payment_method_id,
                                      # trial_end='now',
                                      payment_behavior=payment_behavior,
                                      payment_settings=payment_settings,
                                      expand=expand
                                    )


def cancel_stripe_subscription(subscription_id):
    return stripe.Subscription.modify(subscription_id,
                                      cancel_at_period_end=True
                                      )


def not_cancel_stripe_subscription(subscription_id):
    return stripe.Subscription.modify(subscription_id,
                                      cancel_at_period_end=False
                                      )


def retrieve_customer_subscription(subscription_id):
    return stripe.Subscription.retrieve(subscription_id)


def latest_subscription_invoice(latest_invoice_id):
    return stripe.Invoice.retrieve(latest_invoice_id)


def customer_payment_methods(customer_id):
    return stripe.Customer.list_payment_methods(customer_id, type='card')
