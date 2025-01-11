from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, ProfileSerializer
from .models import Profile
from rest_framework.views import APIView
from .serializers import PostSerializer
from .models import Post,Comment
from django.contrib.auth.models import User
from .models import Notification
from .serializers import NotificationSerializer
from .models import Message
from .serializers import MessageSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register(request):
    """User registration endpoint"""
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """User login endpoint to get JWT tokens"""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """Get the profile of the authenticated user"""
    try:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update the authenticated user's profile"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"message": "Post created successfully", "post_id": serializer.instance.id}, status=201)
        return Response({"error": serializer.errors}, status=400)
    
    
class GetAllPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        if request.user in post.likes.all():
            return Response({"error": "You have already liked this post"}, status=400)

        post.likes.add(request.user)
        return Response({"message": "Post liked successfully"})

class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        content = request.data.get('content')
        if not content:
            return Response({"error": "Content is required"}, status=400)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        comment = Comment.objects.create(post=post, author=request.user, content=content)
        return Response({"message": "Comment added successfully", "comment_id": comment.id})
    

from django.conf import settings

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        User = get_user_model()  # Get the actual user model
        try:
            user_to_follow = User.objects.get(id=user_id)  # Use the user model here
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Prevent users from following themselves
        if user_to_follow == request.user:
            return Response({"error": "You cannot follow yourself"}, status=400)

        # Check if already following
        if user_to_follow in request.user.following.all():
            return Response({"error": "You are already following this user"}, status=400)

        # Add the user to the following list
        request.user.following.add(user_to_follow)
        return Response({"message": "Followed user successfully"})

    
class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve notifications for the authenticated user."""
        notifications = Notification.objects.filter(receiver=request.user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipient_id = request.data.get("recipient_id")
        content = request.data.get("content")

        if not recipient_id or not content:
            return Response({"error": "Recipient ID and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the actual user model
        User = get_user_model()

        try:
            recipient = User.objects.get(id=recipient_id)  # Use the resolved User model
        except User.DoesNotExist:
            return Response({"error": "Recipient not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create the message
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content
        )

        return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
    
class ReceivedMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Query the Message model for all messages where the recipient is the given user_id
        messages = Message.objects.filter(recipient__id=user_id)

        # If no messages are found
        if not messages:
            return Response({"message": "No messages found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Format the messages as a list of dictionaries
        message_data = []
        for message in messages:
            message_data.append({
                "sender": message.sender.username,
                "content": message.content,
                "timestamp": message.timestamp
            })

        return Response({"received_messages": message_data}, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist the refresh token to invalidate it
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
            return Response({"message": "Logged out successfully"}, status=200)

        except Exception as e:
            return Response({"error": f"Error during logout: {str(e)}"}, status=400)
        
        
