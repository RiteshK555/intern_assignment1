from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Event
import datetime

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class EventSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ")
    class Meta:
        model = Event
        fields = '__all__'
