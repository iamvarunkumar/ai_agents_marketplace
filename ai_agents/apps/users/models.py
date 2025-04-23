# E:\Projects\AI Agents\ai_agents\apps\users\models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# Removed: from django.urls import reverse (unless get_absolute_url is needed on User)

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

    # ADDED: ManyToManyField to link users to agents in their workspace
    # We import Agent model as a string 'agentify.Agent' to avoid circular imports
    workspace_agents = models.ManyToManyField(
        'agentify.Agent', # Link to the Agent model in the agentify app
        blank=True, # A user can have an empty workspace
        related_name='users_in_workspace', # How to refer back from Agent to Users
        help_text='Agents added to this user\'s workspace.'
    )


    USERNAME_FIELD = 'email'
    # 'username' is still required by AbstractUser unless customised further
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    """
    Stores additional information related to a CustomUser.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True # Makes the user reference the primary key
    )
    bio = models.TextField(blank=True, help_text='A short biography.')
    # Optional: Add other profile fields like location, website, etc.
    # location = models.CharField(max_length=100, blank=True)
    # website = models.URLField(blank=True)

    def __str__(self):
        # Returns the related user's email - more informative
        return f"{self.user.email}'s Profile"

    # Removed get_absolute_url unless specifically needed and URL named '_detail' exists
    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

