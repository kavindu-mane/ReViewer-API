from django.urls import path ,include
from . views import *

urlpatterns = [
    # if url contains /api those all are redirected to below views
    path('', getRoutes),
    path('register/', RegisterView.as_view()),
    path('user/update/basic/', UpdateBasic.as_view()),
    path('user/update/email/', UpdateEmail.as_view()),
    path('user/update/password/', UpdatePassword.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', GetUserView.as_view()),
    path('login/refresh/', CookieTokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('whoiam/', WhoIAmView.as_view()),
    path('search/<str:search>/', SearchBookView.as_view()),
    path('add-to-wishlist', add_to_wishlist),
    path('books/<str:isbn>/', get_book_details),
    path('wishlist/<int:book_id>/status/', get_wishlist_status),
    path('wishlist/remove/', remove_from_wishlist),
    # if url contains api/admin thos urls redirected to admin url pattern file
    path('admin/', include('api.urls_admin')),
]