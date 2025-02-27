from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.settings import api_settings

class RegisterSerializer(serializers.Serializer):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    HOBBY_CHOICES = [
        ('Sports', 'Sports'),
        ('Reading', 'Reading'),
        ('Music', 'Music'),
        ('Gaming', 'Gaming'),
        ('Traveling', 'Traveling')
    ]

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)  # Single choice
    hobbies = serializers.MultipleChoiceField(choices=HOBBY_CHOICES, required=False)  # Multiple choices
    current_time = serializers.TimeField(format=api_settings.TIME_FORMAT, input_formats=None, default=now().time)
    registered_at = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None, default=now)

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})

        return data

    def create(self, validated_data):
        validated_data.pop('current_time', None)  # Remove non-user fields
        validated_data.pop('registered_at', None)
        validated_data.pop('hobbies', None)  # Remove extra fields not needed for user creation

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
