# E:\Projects\AI Agents\ai_agents\apps\users\views.py

from django.views.generic import TemplateView # Used for simple page rendering
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm # Standard Django login form
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required # Import login_required



# Ensure DRF components are installed and imported if used
try:
    from rest_framework import generics, permissions
    from .serializers import UserSerializer, RegisterSerializer # Make sure these serializers are defined
    DRF_AVAILABLE = True
except ImportError:
    DRF_AVAILABLE = False
    # Define dummy classes if DRF is not installed but referenced,
    # although it's better to ensure DRF is installed if using API views.
    class generics:
        class CreateAPIView: pass
        class RetrieveAPIView: pass
    class permissions:
        AllowAny = None
        IsAuthenticated = None
    # Define dummy serializers if needed, or handle appropriately
    class UserSerializer: pass
    class RegisterSerializer: pass


CustomUser = get_user_model()

# --- API Views (using Django REST Framework) ---
# These handle the actual data processing when forms are submitted via JavaScript
# Ensure DRF is installed for these to work correctly

if DRF_AVAILABLE:
    class RegisterView(generics.CreateAPIView):
        """
        API endpoint for user registration.
        Handles POST requests from the registration form's JavaScript.
        """
        queryset = CustomUser.objects.all()
        permission_classes = (permissions.AllowAny,) # Anyone can attempt registration
        serializer_class = RegisterSerializer

    class UserDetailView(generics.RetrieveAPIView):
        """
        API endpoint to retrieve details of the currently authenticated user.
        Requires JWT authentication. Used to verify login status or get user info.
        """
        queryset = CustomUser.objects.all()
        permission_classes = (permissions.IsAuthenticated,) # Only logged-in users
        serializer_class = UserSerializer

        def get_object(self):
            # Returns the user associated with the request's auth token
            return self.request.user
else:
    # Optional: Add placeholder views or raise errors if DRF is expected but not found
    pass

# --- Standard Django Views (for rendering HTML pages) ---
# These simply display the HTML templates

def home_view(request):
    """
    Renders the site's homepage (templates/home.html).
    """
    context = {}
    return render(request, 'home.html', context)

def register_view(request):
    """
    Handles user registration using standard Django forms.
    GET: Displays the registration form.
    POST: Processes registration data.
    URL: /register/
    """
    if request.method == 'POST':
        # Process the submitted form data
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: Log the user in directly after registration
            # login(request, user)
            messages.success(request, 'Registration successful! You can now log in.')
            # Redirect to the login page after successful registration
            return redirect('login_page') # Use the URL name defined in root urls.py
        else:
            # Form is invalid, re-render the page with the form containing errors
            messages.error(request, 'Please correct the errors below.')
    else: # GET request
        # Display an empty form
        form = CustomUserCreationForm()

    # Prepare context for the template
    context = {'form': form}
    # Render the registration HTML page
    return render(request, 'registration/register.html', context)


def login_view(request):
    """
    Handles user login using standard Django forms.
    GET: Displays the login form.
    POST: Processes login credentials.
    URL: /login/
    """
    if request.method == 'POST':
        # Process the submitted form data
        form = AuthenticationForm(request, data=request.POST) # Use standard AuthenticationForm
        if form.is_valid():
            # Form is valid, try to authenticate the user
            username = form.cleaned_data.get('username') # AuthenticationForm uses 'username' field
            password = form.cleaned_data.get('password')
            # Note: If using email as USERNAME_FIELD, user enters email in the 'username' form field.
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Authentication successful, log the user in
                login(request, user)
                messages.info(request, f"Welcome back, {user.username}!") # Or user.email

                # Redirect to the 'next' page if provided, otherwise to home
                next_url = request.POST.get('next')
                # Basic security check to prevent open redirect
                if not next_url or next_url == request.path or not next_url.startswith('/'):
                    next_url = '/' # Default to home page URL name
                return redirect(next_url)
            else:
                # Authentication failed
                messages.error(request,"Invalid username or password.")
        else:
            # Form validation failed (e.g., fields left blank)
            messages.error(request,"Invalid username or password.") # Keep error generic
    else: # GET request
        # Display an empty form
        form = AuthenticationForm()
        # Pass 'next' parameter to the template if it exists in GET query string
        next_url = request.GET.get('next')
        context = {'form': form, 'next': next_url}
        # Render the login HTML page
        return render(request, 'registration/login.html', context)

def logout_view(request):
    """
    Logs the user out using Django's logout function.
    URL: /logout/
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

@login_required # Decorator ensures only logged-in users can access this view
def dashboard_view(request):
    """
    Renders the user's dashboard page.
    Requires user to be logged in.
    """
    context = {
        'user': request.user
    }
    # CORRECTED: Point to the correct template path
    return render(request, 'registration/dashboard.html', context)
