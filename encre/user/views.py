from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from user.serializers import UserRegistrationSerializer, UserLoginSerializer
from core import models

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {'msg': 'User registered successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'msg': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserLoginView(RetrieveAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            hello = serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            if validated_data.get('token') is None:
                if validated_data.get('validation_error') is not None:
                    error_msg = validated_data['validation_error']
                    return Response(
                        {'validation_error': error_msg},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    error_msg = validated_data['internal_error']
                    return Response(
                        {'internal_error': error_msg},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            return Response(
                {'msg': 'Success to login', 'token': validated_data['token']},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # error from unknown reason: internal server error
            return Response(
                {'internal_error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
