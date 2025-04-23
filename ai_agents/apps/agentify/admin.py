# E:\Projects\AI Agents\ai_agents\apps\agentify\admin.py

from django.contrib import admin
from .models import Agent # Import the Agent model

@admin.register(Agent) # Use the @admin.register decorator
class AgentAdmin(admin.ModelAdmin):
    """
    Admin options for the Agent model.
    """
    # Fields to display in the list view
    list_display = ('name', 'creator', 'is_public', 'created_at', 'updated_at')
    # Fields that can be filtered
    list_filter = ('is_public', 'creator', 'created_at')
    # Fields that can be searched
    search_fields = ('name', 'description', 'short_description', 'creator__username', 'creator__email')
    # Automatically generate the slug from the name field
    prepopulated_fields = {'slug': ('name',)}
    # Fields to make read-only in the admin (like timestamps)
    readonly_fields = ('created_at', 'updated_at')
    # Customize field layout in the add/change forms (optional)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'creator', 'is_public')
        }),
        ('Content', {
            'fields': ('short_description', 'description')
        }),
        # ('Schemas (Optional)', {
        #     'classes': ('collapse',), # Make section collapsible
        #     'fields': ('input_schema', 'output_schema'),
        # }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Make section collapsible
        }),
    )

