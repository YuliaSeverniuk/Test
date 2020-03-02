from django.urls import path, include

from .views import PostsList, PostsDetail, LikesList, UserCreate, clearbit_emails

urlpatterns = [
    path("posts/", PostsList.as_view(), name="posts_list"),
    path("posts/<int:pk>/", PostsDetail.as_view(), name="posts_detail"),
    path("likes/", LikesList.as_view(), name="likes_list"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("auth/", include('rest_auth.urls')),
    path("clearbit/", clearbit_emails, name='clearbit_emails'),
]
