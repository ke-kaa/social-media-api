from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser, Profile, Post, Comment, Notification
from .models import Message

User = get_user_model()  # Dynamically get the active user model

# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User  # Use the custom user model
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']


# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    post_id = serializers.ReadOnlyField(source='id')  # Rename 'id' to 'post_id'

    class Meta:
        model = Post
        fields = ['post_id', 'content', 'author', 'media', 'timestamp', 'likes']
        read_only_fields = ['author', 'timestamp', 'likes']  # Author and timestamp are auto-generated
        depth = 1  # Ensures the 'author' field is serialized as its username


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.ReadOnlyField(source='id')  # Rename 'id' to 'comment_id'
    post_id = serializers.PrimaryKeyRelatedField(source='post.id', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'post_id', 'author_username', 'content', 'timestamp']
        read_only_fields = ['timestamp']
        
        
class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')
    receiver = serializers.CharField(source='receiver.username')

    class Meta:
        model = Notification
        fields = ['notification_type', 'sender', 'receiver', 'content', 'timestamp']
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'content', 'timestamp']
        read_only_fields = ['sender', 'timestamp']
