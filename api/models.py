from django.db import models
from django.contrib.auth.models import AbstractUser

# upload file with renaming files
def upload_to(instance, filename):
    return 'books/{filename}.{ext}'.format(filename=instance.pk , ext = filename.split('.')[-1])

# upload file with renaming files
def upload_to_user(instance, filename):
    return 'users/{filename}.{ext}'.format(filename=instance.pk , ext = filename.split('.')[-1])

# user model : its override the djangp abstract user
class User(AbstractUser):
    id = models.AutoField(primary_key = True)
    email= models.EmailField(max_length=200 , unique=True)
    name = models.CharField(max_length=256)
    password = models.CharField(max_length=1024)
    birth_date = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to=upload_to_user , default="users/default_user.svg")
    created_at = models.DateTimeField(auto_now_add=True)
    username = None
    first_name = None
    last_name = None
    is_staff = None
    date_joined = None

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = [name , email , password , id]

# book model
class Book(models.Model):
    isbn = models.CharField(max_length = 50 , primary_key = True)
    title = models.CharField(max_length = 256)
    author = models.CharField(max_length = 256)
    category = models.CharField(max_length = 256)
    pubyear = models.CharField(max_length = 5)
    language = models.CharField(max_length = 30)
    price = models.CharField(max_length = 10)
    description = models.CharField(max_length = 1024)
    reviews = models.PositiveSmallIntegerField(default = 0)
    reviews_score = models.PositiveSmallIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to=upload_to , default="books/default.png")

    REQUIRED_FIELDS = [isbn , title , author , category , pubyear , language , price , description]

# wish list model
class WishList(models.Model):
    id = models.AutoField(primary_key = True)
    book = models.ForeignKey(Book , on_delete=models.CASCADE)
    user= models.ForeignKey(User , on_delete=models.CASCADE)

#Review Model
class Review(models.Model):
    review = models.TextField(max_length=1024,default=None)
    rate = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book,models.CASCADE,default=None)
    user = models.ForeignKey(User, models.CASCADE,default=None , related_name="review_user")

    REQUIRED_FIELDS = [user , review , rate , book]
