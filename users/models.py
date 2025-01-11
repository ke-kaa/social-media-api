from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    # Define other custom fields here, if necessary
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    # Specify a unique related_name for reverse relationships
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # This fixes the conflict
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # This fixes the conflict
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser_permission'
    )


class Profile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    def __str__(self):
        return self.user.username


# Signal to create Profile automatically after user creation
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Signal to save the Profile instance when the user is saved
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):  # Ensure the profile exists
        instance.profile.save()


class Post(models.Model):
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    media = models.FileField(upload_to='posts/media/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}"
    
class Comment(models.Model):
    
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]

    
User.add_to_class('following', models.ManyToManyField(
    'self',
    symmetrical=False,
    related_name='followers',
    blank=True
))

CustomUser = get_user_model()



class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('mention', 'Mention'),
        # You can add more notification types here
    )
    
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_notifications", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)  # Optional content for the notification
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.sender.username} to {self.receiver.username}"

    




class Message(models.Model):
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.timestamp}"
