from pyexpat import model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.models import Feedback

User = get_user_model()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.IntegerField(required=True, max_value=9999, min_value=1000)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.IntegerField(required=True, max_value=9999, min_value=1000)
    password = serializers.CharField(write_only=True, style={"input_type": 'password'})
    confirm_password = serializers.CharField(write_only=True, style={"input_type": 'password'})


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        exclude = ['status']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'status': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            },
            'updated_at': {
                'read_only': True
            }
        }
