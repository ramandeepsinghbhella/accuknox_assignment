from rest_framework import serializers
from .models import User, FriendRequest
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # This ensures the password is hashed
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'token': token.key
        }

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        data['user'] = user
        return data

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.EmailField(source='from_user.email')
    to_user = serializers.EmailField(source='to_user.email')
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status']
