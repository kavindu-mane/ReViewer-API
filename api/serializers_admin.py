from rest_framework import serializers
from . models import Book
from django.contrib.auth import get_user_model

# book serializer : this one use for adding all functions related to books
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model= Book
        fields = ['isbn', 'title', 'author','category' , 
                  'pubyear' , 'language','price','description' , "cover_image","reviews","reviews_score"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance