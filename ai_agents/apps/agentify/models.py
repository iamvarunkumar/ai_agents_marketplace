# E:\Projects\AI Agents\ai_agents\apps\agentify\models.py

from django.db import models
from django.conf import settings # To link to the custom user model
from django.urls import reverse
from django.utils.text import slugify # Import slugify function

class Agent(models.Model):
    """
    Represents an AI Agent available in the marketplace.
    """
    name = models.CharField(
        max_length=100,
        unique=True, # Ensure agent names are unique
        help_text="The unique name of the AI agent."
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        # Allow blank in forms/admin, but database still requires a value
        blank=True,
        help_text="URL-friendly version of the name, auto-generated if left blank."
    )
    description = models.TextField(
        blank=True,
        help_text="A detailed description of what the agent does."
    )
    short_description = models.CharField(
        max_length=255,
        blank=True,
        help_text="A brief summary shown in list views."
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Links to your CustomUser model
        on_delete=models.SET_NULL, # Keep agent if creator is deleted, set creator to NULL
        null=True, # Allow creator to be NULL in the database
        blank=True, # Allow creator to be blank in forms/admin (e.g., for platform agents)
        related_name='created_agents',
        help_text="The user who created this agent."
    )
    # Add placeholder fields for later
    # input_schema = models.JSONField(null=True, blank=True, help_text="Schema definition for expected input.")
    # output_schema = models.JSONField(null=True, blank=True, help_text="Schema definition for expected output.")
    # version = models.CharField(max_length=20, default='1.0')
    is_public = models.BooleanField(
        default=True,
        help_text="Is this agent visible to everyone in the marketplace?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name'] # Default ordering by name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Define how to get the URL for a single agent instance
        # Assumes you created an 'agent_detail' URL name in agentify.urls
        # Ensure the name matches: 'agentify:agent_detail'
        try:
            # Use the 'agentify' namespace defined in your root urls.py include
            return reverse('agentify:agent_detail', kwargs={'slug': self.slug})
        except Exception:
             # Fallback or handle error if URL is not defined yet
             return "#" # Return a placeholder if URL doesn't resolve

    def save(self, *args, **kwargs):
        # Override save method to auto-generate slug if it's empty
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness if multiple agents might have the same name initially
            # This basic version might fail if slugify(name) isn't unique.
            # A more robust solution would append numbers/UUIDs if needed.
        super().save(*args, **kwargs) # Call the "real" save() method.

# Add other agent-related models here later (e.g., AgentVersion, AgentRunLog)

