from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from core import models

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=64, write_only=True)
    #token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        try:
            user = authenticate(email=email, password=password)
            payload = jwt_payload_handler(user)
            jwt_token = jwt_encode_handler(payload)
            update_last_login(None, user)

        except models.User.DoesNotExist as e:
            return {'validation_error': 'User does not exist.'}
        except Exception as e:
            return {'internal_error': str(e)}

        print("Final part of UserLoginSerializer")
        return {'token': jwt_token}