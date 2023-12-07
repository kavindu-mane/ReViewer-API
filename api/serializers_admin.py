from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("name", "email","birth_date")