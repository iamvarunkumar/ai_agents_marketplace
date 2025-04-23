# E:\Projects\AI Agents\ai_agents\apps\agentify\admin.py

from django.contrib import admin
from .models import Agent # Import the Agent model

@admin.register(Agent) # Use the @admin.register decorator
class AgentAdmin(admin.ModelAdmin):
    """
    Admin options for the Agent model.
    """
    list_display = ('name', 'category', 'tier', 'creator', 'is_public', 'created_at') # Added category
    list_filter = ('is_public', 'tier', 'category', 'creator', 'created_at') # Added category
    search_fields = ('name', 'description', 'short_description', 'creator__username', 'creator__email')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'creator', 'tier', 'category', 'is_public') # Added category
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'illustration')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )