from django.urls import path
from . import views
from . views import RegisterView , LoginView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('',views.getRoutes),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]