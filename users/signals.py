from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from stripe.error import StripeError

from .models import *
from stripe_payment.utils import create_stripe_customer, stripe_customer_delete
from stripe_payment.models import StripePayment


# @receiver(post_save, sender=User)
# def user_post_save_signal(sender, instance, created, **kwargs):
#     if created and instance.is_superuser is not True:
#         try:
#             customer = create_stripe_customer(user=instance)
#             import datetime
#             extend_time = datetime.datetime.now()
#             StripePayment.objects.create(
#                 user=instance,
#                 customer_id=customer.id,
#                 paid_until=round(extend_time.timestamp()),
#                 status='-1'  # -1=incomplete, 0=inavtive, 1=active
#             )
#         except StripeError as e:
#             print(e.user_message)
#         except Exception as e:
#             print(e)


# @receiver(pre_delete, sender=User)
# def stripe_customer_pre_delete(sender, instance, *args, **kwargs):
#     stripe_customer = StripePayment.objects.filter(user=instance).first()
#     if stripe_customer:
#         try:
#             stripe_customer_delete(customer_id=stripe_customer.customer_id)
#         except StripeError as e:
#             print(e.user_message)
#         except Exception as e:
#             print(e)
