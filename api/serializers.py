from rest_framework import serializers
from django.contrib.auth import get_user_model
from . models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['email', 'name', 'password','birth_date']
        extra_kwargs={
            'password':{
                'write_only':True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("name", "email","birth_date","avatar")