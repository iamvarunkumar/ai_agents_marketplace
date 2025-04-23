from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.users.serializers import UserSerializer, RegisterSerializer
# SimpleJWT views for login will be handled in urls.py directly

CustomUser = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,) # Anyone can register
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,) # Must be logged in
    serializer_class = UserSerializer

    def get_object(self):
        # Return the currently logged-in user
        return self.request.user
# Create your views here.

def home_view(request):
    """
    Renders the site's homepage.
    """
    # You can add context dictionary here if needed later
    # context = {'some_key': 'some_value'}
    return render(request, 'home.html') # Renders templates/home.html

# E:\Projects\AI Agents\ai_agents\apps\agentify\views.py

from django.shortcuts import render
from django.views.generic import ListView # Use Django's generic ListView
from .models import Agent # Import the Agent model

class AgentListView(ListView):
    """
    Displays a list of publicly available agents.
    """
    model = Agent # Specify the model to use
    template_name = 'agentify/agent_list.html' # Specify the template to render
    context_object_name = 'agents' # Name of the list in the template context
    paginate_by = 12 # Optional: Show 12 agents per page

    def get_queryset(self):
        # Filter to only show public agents, ordered by name
        return Agent.objects.filter(is_public=True).order_by('name')

# You will add other views here later (e.g., AgentDetailView, AgentCreateView)

