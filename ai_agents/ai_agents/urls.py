# E:\Projects\AI Agents\ai_agents\ai_agents\urls.py

from django.contrib import admin
from django.urls import path, include
from apps.users import views as user_views # Import views from the users app

urlpatterns = [
    # --- Page Rendering URLs ---
    path('', user_views.home_view, name='home'), # Homepage
    path('login/', user_views.LoginPageView.as_view(), name='login_page'), # Render login.html
    path('register/', user_views.RegisterPageView.as_view(), name='register_page'), # Render register.html

    # --- Admin Site ---
    path('admin/', admin.site.urls),

    # --- API Endpoints ---
    # Include URLs from the users app, namespaced under 'users_api'
    # All URLs defined in apps.users.urls will be accessible under /api/auth/
    # e.g., /api/auth/register/, /api/auth/login/, /api/auth/me/
    path('api/auth/', include('apps.users.urls', namespace='users_api')),

    # --- Placeholder for Agentify App URLs ---
    # Uncomment and configure later when agentify app has URLs
    # path('api/agents/', include('apps.agentify.urls', namespace='agentify_api')),

    # Add other top-level paths or includes as needed
]

# Configuration for serving media files during development (optional)
# from django.conf import settings
# from django.conf.urls.static import static
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

