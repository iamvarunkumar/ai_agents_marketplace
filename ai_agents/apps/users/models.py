from django.db import models
from django.conf import settings # Good practice to import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom User model inheriting from AbstractUser, using email as the
    primary identifier.
    """
    email = models.EmailField(
        unique=True,
        help_text='Required. Use email for login.'
        )
    # Optional: Add other fields like profile picture, etc.
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    # 'username' is still needed by AbstractUser unless customised further
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    """
    Stores additional information related to a CustomUser.
    Linked OneToOne with the user.
    """
    # Use settings.AUTH_USER_MODEL to refer to your CustomUser indirectly
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True # Makes the user link the primary key
        )
    bio = models.TextField(blank=True, help_text='A short biography.')
    # Optional: Add other profile fields like location, website, etc.
    # location = models.CharField(max_length=100, blank=True)
    # website = models.URLField(blank=True)

    def __str__(self):
        # Returns the related user's email
        return f"{self.user.email}'s Profile"