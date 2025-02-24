from django.contrib.auth import authenticate
from .models import User
from rest_framework import serializers
from .models import SpamNumber

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        return user

class SpamNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamNumber
        fields = ['phone_number']

    def create(self, validated_data):
        spam_number = SpamNumber.objects.create(**validated_data)
        return spam_number
