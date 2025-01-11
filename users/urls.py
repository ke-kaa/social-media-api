from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CreatePostView
from .views import GetAllPostsView
from .views import LikePostView
from .views import AddCommentView
from .views import FollowUserView
from .views import NotificationListView
from .views import SendMessageView
from .views import ReceivedMessagesView
from .views import LogoutView


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.get_profile, name='get_profile'),  # Get profile
    path('profile/update/', views.update_profile, name='update_profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Adjusted refresh token endpoint
    path('posts/create', CreatePostView.as_view(), name='create-post'),  # Adjusted post endpoint
    path('posts/', GetAllPostsView.as_view(), name='get-all-posts'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('messages/', SendMessageView.as_view(), name='send_message'),
    path('messages/received/<int:user_id>/', ReceivedMessagesView.as_view(), name='received_messages'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]
