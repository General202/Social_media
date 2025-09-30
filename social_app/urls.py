from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
]