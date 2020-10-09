from django.urls import path
from .views import HumanView, HumanStatisticsView, LoadPageView, RoomsView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from app import views


urlpatterns = [
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('human/', HumanView.as_view(), name='human_view'),
    path('statistics/', HumanStatisticsView.as_view(), name='human_statistics_view'),
    path('loadpage/', LoadPageView.as_view(), name='loadpage'),
    path('rooms/', RoomsView.as_view(), name='rooms'),
]