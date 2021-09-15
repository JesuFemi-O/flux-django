from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView, AllUsers, UserDetail, UserProfile, MyTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('users/', AllUsers.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('profile/', UserProfile.as_view(), name='profile-detail')
]
