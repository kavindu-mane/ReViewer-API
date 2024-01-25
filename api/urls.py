from django.urls import path ,include
from . views import *

urlpatterns = [
    # if url contains /api those all are redirected to below views
    path('', getRoutes),
    path('register', RegisterView.as_view()),
    path('profile_update', DetailUpdateProfile.as_view()),
    path('profile_password', ChangePasswordView.as_view()),
    path('login', LoginView.as_view()),
    path('user', GetUserView.as_view()),
    path('login/refresh', CookieTokenRefreshView.as_view()),
    path('logout', LogoutView.as_view()),
    path('whoiam', WhoIAmView.as_view()),
    path('search', SearchBookView.as_view()),
    # if url contains api/admin thos urls redirected to admin url pattern file
    path('admin/', include('api.urls_admin')),
]