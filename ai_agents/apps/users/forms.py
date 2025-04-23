# E:\Projects\AI Agents\ai_agents\apps\users\forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # Import base forms
from django.contrib.auth import get_user_model # Function to get the active user model

# Get the CustomUser model defined in settings.AUTH_USER_MODEL
CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password. Overrides the default UserCreationForm to work with the
    CustomUser model, potentially using 'email' as the primary identifier
    if configured in the model.
    """
    class Meta(UserCreationForm.Meta):
        # Specify the model this form is based on
        model = CustomUser
        # Define the fields to include in the registration form.
        # Make sure these fields exist on your CustomUser model.
        # If 'email' is your USERNAME_FIELD, it must be included.
        # 'password' fields are handled automatically by UserCreationForm.
        fields = ('username', 'email') # Add 'first_name', 'last_name' if desired and on model

class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating existing users (e.g., in the admin or a profile page).
    Includes fields from the user model, replacing the password field
    with admin's password hash display field.
    (This form is not strictly needed for basic registration/login but is good practice).
    """
    class Meta(UserChangeForm.Meta):
        # Specify the model this form is based on
        model = CustomUser
        # Define the fields that can be edited. Adjust as needed.
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff') # Example fields

