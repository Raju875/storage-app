from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from datetime import timedelta
from users.models import Feedback, VerificationCode
from utils.time_zones import TimeZoneUtil
from users.api.v1.serializers import ForgotPasswordSerializer, VerificationCodeSerializer, ResetPasswordSerializer, FeedbackSerializer

User = get_user_model()

    
class ForgotPasswordView(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny, ] 
    serializer_class = ForgotPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        user = User.objects.get(email=email)
        if not user:
            return Response({"success": False,
                             "message": _("Your entered email number does not exist. "
                             "Please enter a valid email or Create New Account.")},
                             status=status.HTTP_400_BAD_REQUEST)
        try:
            code = VerificationCode.generate_code_for_user(user)
            email_context = {
                "email": email,
                "code": code
            }
            html_content = render_to_string('forgot_password.html', email_context)

            message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=email,
                subject='Forget Password',
                html_content=html_content)
            sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
            sg.send(message)

            return Response({"success": True, 
                             "message": _("A mail is sent to " + email + ". Please check it."),
                             "data": email_context['email']},
                              status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"success": False, 
                             "message": str(e) + '[UFP-101]'},
                              status=status.HTTP_400_BAD_REQUEST)


class VerificationViewSet(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny, ]
    serializer_class = VerificationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        code = request.data['code']
        user_code = VerificationCode.objects.filter(code=code, is_used=False, user__email=email).first()
        if not user_code:
            return Response({"success": False,
                             "message": _('Invalid Code! Please provide a valid verification code')},
                              status=status.HTTP_400_BAD_REQUEST)

        now = TimeZoneUtil.get_datetime()
        expired_date = TimeZoneUtil.utc_to_timezone(user_code.updated_at + timedelta(minutes=60))
        if expired_date < now:
            return Response({"success": False,
                             "message": _("Token expired!")},
                              status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True, 
                         'data': {"email": email, "code": code}},
                          status=status.HTTP_200_OK)


class ResetPasswordSetView(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        code = request.data['code']
        user_code = VerificationCode.objects.filter(code=code, is_used=False, user__email=email).first()
        if not user_code:
            return Response({"success": False,
                             "message": _('Invalid Code!  Please try again.')},
                              status=status.HTTP_400_BAD_REQUEST)

        expired_date = TimeZoneUtil.utc_to_timezone(user_code.updated_at + timedelta(minutes=60))
        now = TimeZoneUtil.get_datetime()
        if expired_date < now:
            return Response({"success": False,
                             "message": _("Token expired!")}, 
                              status=status.HTTP_400_BAD_REQUEST)

        if request.data['password'] != request.data['confirm_password']:
            return Response({"success": False,
                             "message": _("Those passwords don't match.")}, 
                              status=status.HTTP_400_BAD_REQUEST)
 
        user = user_code.user
        user.set_password(request.data['password'])
        user.save()

        user_code.is_used = True
        user_code.save()

        return Response({"success": True, 
                         "message": _("Password update successfully.")}, 
                          status=status.HTTP_201_CREATED)


class FeedbackViewSet(ModelViewSet):

    http_method_names = ['get', 'post']
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.none()

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user).filter(is_active=True)

    def perform_create(self, serializer):
        try:
            print(self.request.data)
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response(_(str(e) + ' UF-101'), status=status.HTTP_400_BAD_REQUEST)


class DeleteAccount(ModelViewSet):
    http_method_names = ['delete']
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            self.request.user.delete()
        except Exception as e:
            return Response(_(str(e) + ' UD-101'), status=status.HTTP_400_BAD_REQUEST)

        return Response("User delete", status=status.HTTP_204_NO_CONTENT)
