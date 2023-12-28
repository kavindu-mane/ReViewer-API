from rest_framework import serializers
from . models import Book
from django.contrib.auth import get_user_model

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("name", "email","birth_date")

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model= Book
        fields = ['isbn', 'title', 'author','category' , 
                  'pubyear' , 'language','price','description' , "cover_image"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance