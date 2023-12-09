from django.urls import path
from .views_admin import getUsers , changeUserStatus

urlpatterns = [
    path('users', getUsers.as_view()),
    path('users/update', changeUserStatus.as_view()),

]