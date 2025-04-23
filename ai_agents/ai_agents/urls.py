# E:\Projects\AI Agents\ai_agents\ai_agents\urls.py

from django.contrib import admin
from django.urls import path, include
# Import views directly from the users app
from apps.users import views as user_views

urlpatterns = [
    # --- Page Rendering & Form Handling URLs ---
    # These URLs use the standard Django views defined above
    path('', user_views.home_view, name='home'),             # Homepage view
    path('login/', user_views.login_view, name='login_page'), # Login view (GET/POST)
    path('register/', user_views.register_view, name='register_page'), # Register view (GET/POST)
    path('logout/', user_views.logout_view, name='logout_page'), # Logout view
    path('dashboard/', user_views.dashboard_view, name='dashboard_view'), # Name is 'dashboard_view' # Dashboard Page

    # --- Admin Site ---
    # path('admin/', admin.site.urls), # Still commented out

    # --- API Endpoints (Optional - For other user actions) ---
    # Include URLs from the users app, perhaps for profile management later
    # If you don't plan any other user-related API endpoints soon, you can comment this out too.
    # path('api/users/', include('apps.users.urls', namespace='users_api')), # Commented out during debug

    # --- Placeholder for Agentify App URLs ---
    # path('api/agents/', include('apps.agentify.urls', namespace='agentify_api')), # For agent-related APIs

]

# --- Development Static/Media File Serving (Optional) ---
# from django.conf import settings
# from django.conf.urls.static import static
# if settings.DEBUG:
#     # Add URL patterns for serving static files during development
#     # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Usually handled automatically if DEBUG=True
#     # Add URL patterns for serving media files during development
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)