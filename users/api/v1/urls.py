from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("forgot-password", views.ForgotPasswordView, basename="forgot_password")
router.register("code-verification", views.VerificationViewSet, basename="code_verification")
router.register("reset-password", views.ResetPasswordSetView, basename="reset_password")
router.register("delete-account", views.DeleteAccount, basename="delete_account")

router.register("feedback", views.FeedbackViewSet, basename="feedback")

urlpatterns = [
    path("", include(router.urls)),
]
