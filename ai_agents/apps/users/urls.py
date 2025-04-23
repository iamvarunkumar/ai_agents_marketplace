# E:\Projects\AI Agents\ai_agents\apps\users\urls.py

from django.urls import path
# Import views from this app if needed for user-specific pages later
# from . import views

app_name = 'users' # Namespace for user-related URLs (e.g., profile)

urlpatterns = [
    # This list should be empty for now, unless you have specific user
    # pages like profiles already defined in apps/users/views.py.
    # Do NOT include home, login, register, logout, or the 'api/users/' include here.

    # Example of what might go here later:
    # path('profile/', views.profile_view, name='profile'),
    # path('profile/edit/', views.profile_edit_view, name='profile_edit'),
]

# Removed incorrect imports and patterns from the user's pasted code.