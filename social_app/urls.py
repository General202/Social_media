from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
]