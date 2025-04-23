# E:\Projects\AI Agents\ai_agents\apps\agentify\models.py

from django.db import models
from django.conf import settings # Good practice if linking to User model

# --- Add Agent-related models below ---

# Example (Uncomment and modify when ready to define Agent models):
class Agent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Use setting to refer to CustomUser
        on_delete=models.SET_NULL, # Or CASCADE, PROTECT based on requirements
        related_name='created_agents',
        null=True # Allow agents without creators? Or remove null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add other fields like version, status, input_schema, output_schema etc.

    def __str__(self):
        return self.name

# Keep this file, even if empty for now (besides the 'from django.db import models'),
# until you are ready to add agent-specific models.