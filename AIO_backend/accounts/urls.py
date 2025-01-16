from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    SignupView, 
    LogoutView,
    ProfileView, 
    ProfileUpdateView, 
    DeleteUserView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', obtain_auth_token, name='login'),  # DRF Token 로그인
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
]