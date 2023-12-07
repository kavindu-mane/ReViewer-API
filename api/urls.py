from django.urls import path ,include
from . views import RegisterView , LoginView , LogoutView , getRoutes , CookieTokenRefreshView , GetUser

urlpatterns = [
    path('', getRoutes),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', GetUser.as_view()),
    path('login/refresh', CookieTokenRefreshView.as_view()),
    path('logout', LogoutView.as_view()),
    path('admin/', include('api.urls_admin')),
]