from django.urls import path

from .views import *

app_name = 'stripe_payment'
urlpatterns = [
    # path('test/apple-pay/', ApplePayTestView.as_view()),
    path('test/google-pay/', GooglePayTestView.as_view()),
]
