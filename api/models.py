from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email= models.EmailField(max_length=200 , primary_key=True)
    name = models.CharField(max_length=256)
    password = models.CharField(max_length=1024)
    birth_date = models.CharField(max_length=30)
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [name , email , password]
