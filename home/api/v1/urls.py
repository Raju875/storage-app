from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet,
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")

urlpatterns = [
    path("", include(router.urls)),
    # path('login/social/google/', views.GoogleLoginAPI.as_view(), name="google_login"),
    # path('login/social/google/connect/', views.GoogleLoginConnectAPI.as_view(), name="google_login_connect"),
    # path('login/social/facebook/', views.FacebookLoginAPI.as_view(), name="facebook_login"),
    # path('login/social/facebook/connect/', views.FacebookLoginConnectAPI.as_view(), name="facebook_login_connect"),
]
