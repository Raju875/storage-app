# from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from django.conf import settings
# from rest_auth.registration.views import SocialLoginView, SocialConnectView
# from .serializers import CustomSocialAuthSerializer, CustomTokenSerializer
#
#
# class CustomSocialLoginView(SocialLoginView):
#     authentication_classes = []
#     permission_classes = []
#     serializer_class = CustomSocialAuthSerializer
#
#     def get_response_serializer(self):
#         if getattr(settings, 'REST_USE_JWT', False):
#             from rest_auth.serializers import JWTSerializer
#             response_serializer = JWTSerializer
#         else:
#             response_serializer = CustomTokenSerializer
#         return response_serializer
#
#
# class FacebookLoginAPI(CustomSocialLoginView):
#     adapter_class = FacebookOAuth2Adapter
#
#
# class GoogleLoginAPI(CustomSocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#
#
# class AppleLoginAPI(CustomSocialLoginView):
#     adapter_class = AppleOAuth2Adapter
#
#
# class FacebookLoginConnectAPI(SocialConnectView):
#     # authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAuthenticated]
#     adapter_class = FacebookOAuth2Adapter
#
#
# class GoogleLoginConnectAPI(SocialConnectView):
#     # authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAuthenticated]
#     adapter_class = GoogleOAuth2Adapter
#
#
# class AppleLoginConnectAPI(SocialConnectView):
#     # authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAuthenticated]
#     adapter_class = AppleOAuth2Adapter
