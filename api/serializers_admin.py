from rest_framework import serializers
from . models import Book
from .models import User

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
    
# user account serializer : this use for return users data in admin panel
class UserAccountSerializer(serializers.ModelSerializer):
    review_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["name", "email","birth_date" , "review_user"]

    def get_review_user(self, obj):
        return obj.review_user.count()