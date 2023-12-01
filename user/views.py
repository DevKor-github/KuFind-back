from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC



from django.shortcuts import render
from rest_framework import status, mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .serializers import *
from .models import *


# class ConfirmEmailView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, *args, **kwargs):
#         self.object = confirmation = self.get_object()
#         confirmation.confirm(self.request)
#         # A React Router Route will handle the failure scenario
#         return HttpResponseRedirect('/login/')
#
#     def get_object(self, queryset=None):
#         key = self.kwargs['key']
#         email_confirmation = EmailConfirmationHMAC.from_key(key)
#         if not email_confirmation:
#             if queryset is None:
#                 queryset = self.get_queryset()
#             try:
#                 email_confirmation = queryset.get(key=key.lower())
#             except EmailConfirmation.DoesNotExist:
#                 return HttpResponseRedirect('/login/')
#         return email_confirmation
#
#     def get_queryset(self):
#         qs = EmailConfirmation.objects.all_valid()
#         qs = qs.select_related("email_address__user")
#         return qs
#
#
# from user.serializers import (
#     UserSerializer,
#     AuthTokenSerializer,
# )
#
#
# class CreateUserView(generics.CreateAPIView):
#     #Create a new user in the system.
#     serializer_class = UserSerializer
#
#
# class CreateTokenView(ObtainAuthToken):
#     #Create a new auth token for user.
#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
#
#
# class ManageUserView(generics.RetrieveUpdateAPIView):
#     #Manage the authenticated user.
#     serializer_class = UserSerializer
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         #Retrieve and return the authenticated user.
#         return self.request.user


@permission_classes([AllowAny])
class Registration(generics.GenericAPIView):
    serializer_class = CustomRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data
            },
            status=status.HTTP_201_CREATED,
        )


@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user['email'] == "None":
            return Response({"message": "fail"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": user['token']
            }
        )