# E:\Projects\AI Agents\ai_agents\apps\users\admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm # Import your custom forms
from .models import UserProfile # Import UserProfile if you want it in admin

CustomUser = get_user_model()

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False # Don't allow deleting profile from user admin
    verbose_name_plural = 'Profile'
    fk_name = 'user' # Explicitly specify the foreign key name

# Define a new User admin
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # Fields shown in the list view of users
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active']
    # Fields that can be filtered in the right sidebar
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    # Fields that can be searched
    search_fields = ['email', 'username', 'first_name', 'last_name']
    # How the fields are ordered
    ordering = ['email']
    # Define fieldsets for the add/change forms
    # This structure is inherited from UserAdmin and adapted for CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'password')}), # Use email instead of username here
        ('Personal info', {'fields': ('first_name', 'last_name', 'username')}), # Keep username if needed
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # Add custom fields here if any (e.g., user_type from previous examples)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        # Add custom fields to the creation form if needed
        (None, {'fields': ('email',)}), # Ensure email is prominent
    )
    # Add the profile inline so you can edit profile fields within the user admin page
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# Register your CustomUser model with the custom admin options
admin.site.register(CustomUser, CustomUserAdmin)

# Optional: Register UserProfile separately if you want a dedicated section for it
# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'bio') # Example fields
#     search_fields = ('user__email', 'user__username')

