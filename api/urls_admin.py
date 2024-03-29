from django.urls import path
from .views_admin import *

# urls for admin : this will redirect if requested url start with api/admim
urlpatterns = [
    path('users/', getUsers.as_view()),
    path('users/update/', changeUserStatus.as_view()),
    path('books/add/', addNewBook.as_view()),
    path('books/', getBooks.as_view()),
    path('dashboard/<str:type>/', GetAdminStats.as_view()),

]