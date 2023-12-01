from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_auth.registration.serializers import RegisterSerializer

from .models import *


# class UserSerializer(serializers.ModelSerializer):
#     """Serializer for the user object."""
#
#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'password', 'name']
#         extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
#
#     def create(self, validated_data):
#         """Create and return a user with encrypted password."""
#         return get_user_model().objects.create_user(**validated_data)
#
#     def update(self, instance, validated_data):
#         """Update and return user."""
#         password = validated_data.pop('password', None)
#         user = super().update(instance, validated_data)
#
#         if password:
#             user.set_password(password)
#             user.save()
#
#         return user
#
#
# class AuthTokenSerializer(serializers.Serializer):
#     """Serializer for the user auth token."""
#     email = serializers.EmailField()
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#     )
#
#     def validate(self, attrs):
#         """Validate and authenticate the user."""
#         email = attrs.get('email')
#         password = attrs.get('password')
#         user = authenticate(
#             request=self.context.get('request'),
#             username=email,
#             password=password,
#         )
#         if not user:
#             msg = _('Unable to authenticate with provided credentials.')
#             raise serializers.ValidationError(msg, code='authorization')
#
#         attrs['user'] = user
#         return attrs


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

# 회원가입
class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=False, max_length=50)
    email = serializers.CharField(required=False, max_length=200)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        data_dict['email'] = self.validated_data.get('email', '')

        return data_dict


# 로그인
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password", None)
        # 사용자 아이디와 비밀번호로 로그인 구현(<-> 사용자 아이디 대신 이메일로도 가능)
        user = authenticate(email=email, password=password)

        if user is None:
            return {'email': 'None'}
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exist'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }


# 사용자 정보 추출
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'nickname')