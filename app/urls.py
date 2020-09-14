from django.urls import path
from .views import PostView, HumanView, CreateUserAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from app import views


urlpatterns = [
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('posts/', PostView.as_view(), name='post_view'),
    path('human/', HumanView.as_view(), name='human_view'),
    path('create/', CreateUserAPIView.as_view())
]