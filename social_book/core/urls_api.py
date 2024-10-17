from django.urls import path
from . import views_api  

urlpatterns = [
    path('posts/', views_api.post_list, name='post_list'),  # List/create posts
    path('posts/<int:post_id>/like/', views_api.like_post, name='like_post_api'),  # Like/unlike a post by post ID
    path('profile/<str:username>/', views_api.profile_detail, name='profile_detail_api'),  # Get user profile by username
    path('profile/<str:username>/follow/', views_api.follow, name='follow_api'),  # Follow/unfollow a user by username
    path('followers/<str:username>/', views_api.followers_list, name='followers_list_api'),  # Get list of followers for a user
    path('following/<str:username>/', views_api.following_list, name='following_list_api'),  # Get list of users that a user is following
]

