from django.urls import path
from .views_admin import getUsers

urlpatterns = [
    path('users', getUsers.as_view()),

]