from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.users.serializers import UserSerializer, RegisterSerializer
from django.views.generic import ListView, DetailView # Use Django's generic ListView
from .models import Agent # Import the Agent model
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
# E:\Projects\AI Agents\ai_agents\apps\agentify\views.py

class AgentDetailView(DetailView):
    """
    Displays the details of a single agent.
    Accessed via /agents/<slug>/ URL.
    """
    model = Agent
    template_name = 'agentify/agent_detail.html'
    context_object_name = 'agent' # Name for the single agent object in the template
    # DetailView automatically uses the 'slug' field from the URL pattern
    # if slug_field is not specified otherwise, or pk if pk is used in URL.
    slug_field = 'slug' # Explicitly state we are looking up by slug
    slug_url_kwarg = 'slug' # Explicitly state the URL keyword argument is 'slug'

    def get_queryset(self):
        # Optionally, ensure only public agents can be viewed directly
        # Or allow creators to view their non-public agents (add logic later)
        return Agent.objects.filter(is_public=True)

# You will add other views here later (e.g., AgentCreateView)
