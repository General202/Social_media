from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('friend-request/accept/<int:user_id>/', views.AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('friend/remove/<int:user_id>/', views.RemoveFriendView.as_view(), name='remove_friend'),
    path('search/users/', views.UserSearchView.as_view(), name='user_search'),
    path('friend-request/create/<int:user_id>/', views.CreateFriendRequestView.as_view(), name='create_friend_request'),
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/create/', views.GroupCreateView.as_view(), name='create_group'),
    path('groups/<int:pk>/', views.GroupDetailView.as_view(), name='group_detail'),
    path('groups/<int:pk>/join/', views.JoinGroupView.as_view(), name='join_group'),
    path('groups/<int:pk>/leave/', views.LeaveGroupView.as_view(), name='leave_group'),
    path('groups/<int:pk>/post/create/', views.GroupPostCreateView.as_view(), name='create_group_post'),
]