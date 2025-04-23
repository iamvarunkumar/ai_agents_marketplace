# E:\Projects\AI Agents\ai_agents\apps\agentify\views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView # Import DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from .models import Agent # Import the Agent model
import google.generativeai as genai
import os
from django.conf import settings

try:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        print("Warning: GOOGLE_API_KEY environment variable not set.")
        # Handle missing key appropriately - maybe disable AI features
    genai.configure(api_key=GOOGLE_API_KEY)
    # Create the model instance (e.g., 'gemini-1.5-flash' or 'gemini-pro')
    # Choose a model appropriate for your task
    model = genai.GenerativeModel('gemini-1.5-flash')
    GEMINI_CONFIGURED = True
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    GEMINI_CONFIGURED = False
    model = None
    
# --- Helper function to parse simple AI list responses ---
def parse_ai_list_response(text_response):
    """Splits text response by newline and cleans up list items."""
    items = [item.strip() for item in text_response.strip().split('\n') if item.strip()]
    # Remove leading list markers like -, *, 1., etc.
    cleaned_items = []
    for item in items:
        match = re.match(r'^[\s*-•\d]+\.?\s*(.*)', item)
        if match:
            cleaned_items.append(match.group(1).strip())
        else:
            cleaned_items.append(item)
    return cleaned_items

# --- Existing Views ---

class AgentListView(ListView):
    """
    Displays a list of publicly available agents.
    Accessed via the /agents/ URL.
    Renders the template 'agentify/agent_list.html'.
    """
    model = Agent # Specifies the model to fetch data from (even if template overrides display)
    template_name = 'agentify/agent_list.html' # Points to the template with the hardcoded cards
    context_object_name = 'agents' # Provides the fetched agents (currently unused by template)
    paginate_by = 12 # Pagination logic still applies if uncommented in template

    def get_queryset(self):
        # This still runs, fetching agents from DB, but template ignores the result for now
        return Agent.objects.filter(is_public=True).order_by('name')

class AgentDetailView(DetailView):
    """Displays the details of a single agent."""
    model = Agent
    template_name = 'agentify/agent_detail.html'
    context_object_name = 'agent'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Agent.objects.filter(is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent = self.get_object()
        if self.request.user.is_authenticated:
            context['in_workspace'] = self.request.user.workspace_agents.filter(pk=agent.pk).exists()
        else:
            context['in_workspace'] = False
        return context

@login_required
@require_POST
def add_to_workspace(request, agent_slug):
    """Adds a specific agent to the logged-in user's workspace."""
    agent = get_object_or_404(Agent, slug=agent_slug, is_public=True)
    request.user.workspace_agents.add(agent)
    messages.success(request, f"'{agent.name}' added to your workspace.")
    return redirect('agentify:agent_detail', slug=agent_slug)

@login_required
@require_POST
def remove_from_workspace(request, agent_slug):
    """Removes a specific agent from the logged-in user's workspace."""
    agent = get_object_or_404(Agent, slug=agent_slug)
    request.user.workspace_agents.remove(agent)
    messages.info(request, f"'{agent.name}' removed from your workspace.")
    return redirect('agentify:agent_detail', slug=agent_slug)

# @login_required # Optional: Decide if tool usage requires login
def blog_idea_generator_view(request):
    """
    Handles the Blog Post Idea Generator tool page.
    GET: Displays the input form.
    POST: Processes the topic and displays generated ideas (mocked for now).
    """
    context = {
        'page_title': 'Blog Post Idea Generator',
        'generated_ideas': None # Start with no results
    }
    agent_slug = 'blog-post-idea-generator' # Define a slug for this tool

    # Fetch the corresponding Agent object to display its info (optional)
    try:
        # Ensure the agent exists in the database with this exact slug
        agent = Agent.objects.get(slug=agent_slug)
        context['agent'] = agent
    except Agent.DoesNotExist:
        context['agent'] = None # Handle case where agent isn't in DB yet
        messages.warning(request, f"Agent data for '{agent_slug}' not found. Please add it via the admin.")


    if request.method == 'POST':
        topic = request.POST.get('topic', '').strip()
        context['submitted_topic'] = topic # Pass submitted topic back to template

        if topic:
            # ** Placeholder for actual AI logic **
            # Replace this with your actual call to an AI model/service
            # Example: ideas_list = call_my_ai_service(topic)
            mock_ideas = [
                f"5 Common Mistakes When Discussing '{topic.title()}'",
                f"The Ultimate Guide to Getting Started with '{topic.title()}'",
                f"'{topic.title()}' in 2025: Key Trends to Watch",
                f"How '{topic.title()}' is Changing [Related Industry]",
                f"Interview with an Expert on '{topic.title()}'"
            ]
            context['generated_ideas'] = mock_ideas
            messages.success(request, "Blog post ideas generated!")
        else:
            # Handle empty topic submission
            messages.error(request, "Please enter a topic to generate ideas.")
            context['generated_ideas'] = [] # Ensure results area shows but is empty

    # Render the specific template for this tool
    return render(request, 'agentify/tools/blog_idea_generator.html', context)

# @login_required
def product_description_writer_view(request):
    """
    Handles the Product Description Writer tool page.
    GET: Displays the input form.
    POST: Processes product info and displays generated descriptions (mocked).
    """
    context = {
        'page_title': 'Product Description Writer',
        'generated_descriptions': None
    }
    agent_slug = 'product-description-writer' # Define slug for this tool

    try:
        agent = Agent.objects.get(slug=agent_slug)
        context['agent'] = agent
    except Agent.DoesNotExist:
        context['agent'] = None
        messages.warning(request, f"Agent data for '{agent_slug}' not found. Please add it via the admin.")

    if request.method == 'POST':
        product_name = request.POST.get('product_name', '').strip()
        features = request.POST.get('features', '').strip()
        audience = request.POST.get('audience', '').strip()
        context['submitted_product'] = product_name # Pass back submitted data

        if product_name and features:
            # ** Placeholder for actual AI logic **
            # Replace with call to AI service: call_ai_desc(product_name, features, audience)
            mock_descriptions = [
                f"Introducing the amazing {product_name}! Perfect for {audience}, it boasts {features.split(',')[0].strip()} and much more. Get yours today!",
                f"Upgrade your experience with the {product_name}. Designed for {audience}, its key benefit is {features}. Don't miss out!",
                f"Meet {product_name}: Combining {features} to deliver outstanding results for {audience}."
            ]
            context['generated_descriptions'] = mock_descriptions
            messages.success(request, "Product descriptions generated!")
        else:
            messages.error(request, "Please enter at least a product name and some features.")
            context['generated_descriptions'] = []

    return render(request, 'agentify/tools/product_description_writer.html', context)

# E:\Projects\AI Agents\ai_agents\apps\agentify\views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from .models import Agent # Import the Agent model

# --- Existing Views ---

class AgentListView(ListView):
    """Displays a list of publicly available agents."""
    model = Agent
    template_name = 'agentify/agent_list.html'
    context_object_name = 'agents'
    paginate_by = 12

    def get_queryset(self):
        return Agent.objects.filter(is_public=True).order_by('name')

class AgentDetailView(DetailView):
    """Displays the details of a single agent."""
    model = Agent
    template_name = 'agentify/agent_detail.html'
    context_object_name = 'agent'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Agent.objects.filter(is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent = self.get_object()
        if self.request.user.is_authenticated:
            context['in_workspace'] = self.request.user.workspace_agents.filter(pk=agent.pk).exists()
        else:
            context['in_workspace'] = False
        return context

@login_required
@require_POST
def add_to_workspace(request, agent_slug):
    """Adds a specific agent to the logged-in user's workspace."""
    agent = get_object_or_404(Agent, slug=agent_slug, is_public=True)
    request.user.workspace_agents.add(agent)
    messages.success(request, f"'{agent.name}' added to your workspace.")
    return redirect('agentify:agent_detail', slug=agent_slug)

@login_required
@require_POST
def remove_from_workspace(request, agent_slug):
    """Removes a specific agent from the logged-in user's workspace."""
    agent = get_object_or_404(Agent, slug=agent_slug)
    request.user.workspace_agents.remove(agent)
    messages.info(request, f"'{agent.name}' removed from your workspace.")
    return redirect('agentify:agent_detail', slug=agent_slug)

# --- Tool Views ---

@login_required
def blog_idea_generator_view(request):
    """Handles the Blog Post Idea Generator tool page, using Gemini AI."""
    context = {'page_title': 'Blog Post Idea Generator', 'generated_ideas': None}
    agent_slug = 'blog-post-idea-generator'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        topic = request.POST.get('topic', '').strip()
        context['submitted_topic'] = topic
        if topic:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Generate 5 distinct blog post ideas (titles or brief outlines) based on the following topic. Format the output as a simple list, with each idea on a new line, starting with a hyphen (-) or number.

Topic: {topic}

Ideas:"""
                    response = model.generate_content(prompt)
                    # Split the response text into a list of ideas
                    ideas_list = [idea.strip() for idea in response.text.strip().split('\n') if idea.strip()]
                    # Remove leading hyphens/numbers if present for cleaner display
                    cleaned_ideas = [idea[2:] if (idea.startswith('- ') or idea.startswith(('. ', ') '))) else idea for idea in ideas_list]
                    context['generated_ideas'] = cleaned_ideas
                    messages.success(request, "Blog post ideas generated using Gemini AI!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['generated_ideas'] = ["Error generating ideas."]
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['generated_ideas'] = ["[AI Service Not Configured - Placeholder Idea 1]"]
        else:
            messages.error(request, "Please enter a topic to generate ideas.")
            context['generated_ideas'] = []
    return render(request, 'agentify/tools/blog_idea_generator.html', context)

# Tool 2: Product Description Writer
# @login_required
def product_description_writer_view(request):
    """Handles the Product Description Writer tool page, using Gemini AI."""
    context = {'page_title': 'Product Description Writer', 'generated_descriptions': None}
    agent_slug = 'product-description-writer'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        product_name = request.POST.get('product_name', '').strip()
        features = request.POST.get('features', '').strip()
        audience = request.POST.get('audience', '').strip()
        context['submitted_product'] = product_name
        context['submitted_features'] = features
        context['submitted_audience'] = audience

        if product_name and features:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Write 3 distinct, engaging product descriptions for the following product. Tailor them for the specified target audience if provided. Highlight the key features. Keep each description relatively short (e.g., 2-4 sentences). Format the output as a list, with each description separated by a blank line.

Product Name: {product_name}
Key Features: {features}
Target Audience: {audience if audience else 'General Audience'}

Descriptions:"""
                    response = model.generate_content(prompt)
                    # Split descriptions by double newlines or handle numbered lists
                    descriptions_list = [desc.strip() for desc in response.text.strip().split('\n\n') if desc.strip()]
                    if len(descriptions_list) <= 1 and '\n1.' in response.text: # Handle numbered lists if split fails
                        descriptions_list = [item.split('.', 1)[1].strip() for item in response.text.strip().split('\n') if item.strip()]

                    context['generated_descriptions'] = descriptions_list[:3] # Limit to 3
                    messages.success(request, "Product descriptions generated using Gemini AI!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['generated_descriptions'] = ["Error generating descriptions."]
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['generated_descriptions'] = ["[AI Service Not Configured - Placeholder Desc 1]"]
        else:
            messages.error(request, "Please enter at least a product name and some features.")
            context['generated_descriptions'] = []
    return render(request, 'agentify/tools/product_description_writer.html', context)

# Tool 3: Social Media Post Creator
# @login_required
def social_media_post_creator_view(request):
    """Handles the Social Media Post Creator tool page, using Gemini AI."""
    context = {'page_title': 'Social Media Post Creator', 'generated_posts': None}
    agent_slug = 'social-media-post-creator'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        platform = request.POST.get('platform', 'twitter')
        context['submitted_text'] = input_text
        context['selected_platform'] = platform

        if input_text:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Generate 3 short, catchy social media posts suitable for {platform.capitalize()} based on the following input text or link. Include relevant hashtags. Format as a list, each post separated by a blank line.

Input: {input_text}

Posts:"""
                    response = model.generate_content(prompt)
                    posts_list = [post.strip() for post in response.text.strip().split('\n\n') if post.strip()]
                    if len(posts_list) <= 1 and '\n1.' in response.text: # Handle numbered lists
                        posts_list = [item.split('.', 1)[1].strip() for item in response.text.strip().split('\n') if item.strip()]

                    context['generated_posts'] = posts_list[:3] # Limit to 3
                    messages.success(request, f"{platform.capitalize()} posts generated using Gemini AI!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['generated_posts'] = ["Error generating posts."]
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['generated_posts'] = ["[AI Service Not Configured - Placeholder Post 1]"]
        else:
            messages.error(request, "Please provide some input text or a link.")
            context['generated_posts'] = []
    return render(request, 'agentify/tools/social_media_post_creator.html', context)

# Tool 4: Email Subject Line Generator
# @login_required
def email_subject_generator_view(request):
    """Handles the Email Subject Line Generator tool page, using Gemini AI."""
    context = {'page_title': 'Email Subject Line Generator', 'generated_subjects': None}
    agent_slug = 'email-subject-line-generator'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        email_body = request.POST.get('email_body', '').strip()
        context['submitted_body'] = email_body
        if email_body:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Generate 5 effective and varied email subject lines based on the following email body snippet. Format as a simple list, each subject on a new line.

Email Body Snippet:
---
{email_body[:500]}...
---

Subject Lines:""" # Limit body length sent to AI
                    response = model.generate_content(prompt)
                    subjects_list = [subj.strip() for subj in response.text.strip().split('\n') if subj.strip()]
                    # Remove leading hyphens/numbers if present
                    cleaned_subjects = [subj[2:] if (subj.startswith('- ') or subj.startswith(('. ', ') '))) else subj for subj in subjects_list]
                    context['generated_subjects'] = cleaned_subjects[:5] # Limit to 5
                    messages.success(request, "Email subject lines generated using Gemini AI!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['generated_subjects'] = ["Error generating subjects."]
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['generated_subjects'] = ["[AI Service Not Configured - Placeholder Subject 1]"]
        else:
            messages.error(request, "Please paste some email body text.")
            context['generated_subjects'] = []
    return render(request, 'agentify/tools/email_subject_generator.html', context)

# Tool 5: Meeting Summarizer
# @login_required
def meeting_summarizer_view(request):
    """Handles the Meeting Summarizer tool page, using Gemini AI."""
    context = {'page_title': 'Meeting Summarizer', 'generated_summary': None}
    agent_slug = 'meeting-summarizer'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        meeting_text = request.POST.get('meeting_text', '').strip()
        context['submitted_text'] = meeting_text
        if meeting_text:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Summarize the following meeting transcript or notes. Identify the main topic, key discussion points, decisions made, and any action items. Format the output clearly, perhaps using Markdown for headings (like ## Key Points) and bullet points.

Meeting Text:
---
{meeting_text}
---

Summary:"""
                    response = model.generate_content(prompt)
                    # Render the markdown response to HTML safely
                    summary_html = markdown.markdown(response.text, extensions=['extra', 'nl2br', 'sane_lists'])
                    context['generated_summary'] = summary_html # Store as HTML
                    messages.success(request, "Meeting summary generated using Gemini AI!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['generated_summary'] = "<p>Error generating summary.</p>"
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['generated_summary'] = "<p>[AI Service Not Configured - Placeholder Summary]</p>"
        else:
            messages.error(request, "Please paste the meeting transcript or notes.")
            context['generated_summary'] = "" # Indicate validation failure
    return render(request, 'agentify/tools/meeting_summarizer.html', context)

@login_required
def sentiment_analysis_view(request):
    """Handles the Sentiment Analysis tool page, using Gemini AI."""
    context = {'page_title': 'Sentiment Analysis Agent', 'analysis_result': None}
    agent_slug = 'sentiment-analysis-agent'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        context['submitted_text'] = input_text
        if input_text:
            if GEMINI_CONFIGURED and model:
                try:
                    # Ask Gemini for sentiment and a confidence score (if possible)
                    prompt = f"""Analyze the sentiment of the following text. Respond with only one word: Positive, Negative, or Neutral. Optionally, add a confidence score from 0.0 to 1.0 after a colon if you can estimate it. Example: Positive: 0.9

Text: "{input_text}"

Sentiment:"""
                    response = model.generate_content(prompt)
                    result_text = response.text.strip()
                    sentiment = "Neutral" # Default
                    score = None
                    if ':' in result_text:
                        parts = result_text.split(':', 1)
                        sentiment = parts[0].strip().capitalize()
                        try:
                            score = float(parts[1].strip())
                        except ValueError:
                            score = None # Couldn't parse score
                    else:
                        sentiment = result_text.capitalize() # Assume only sentiment word returned

                    # Basic validation of sentiment word
                    if sentiment not in ["Positive", "Negative", "Neutral"]:
                        sentiment = "Unknown" # Handle unexpected AI response

                    context['analysis_result'] = {'sentiment': sentiment, 'score': score}
                    messages.success(request, "Sentiment analysis complete (Gemini AI)!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['analysis_result'] = {'sentiment': 'Error', 'score': None}
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['analysis_result'] = {'sentiment': 'Placeholder', 'score': 0.5}
        else:
            messages.error(request, "Please enter text to analyze.")
            context['analysis_result'] = {} # Indicate validation failure
    return render(request, 'agentify/tools/sentiment_analysis.html', context)

# Tool 7: Keyword Extractor
# @login_required
def keyword_extractor_view(request):
    """Handles the Keyword Extractor tool page, using Gemini AI."""
    context = {'page_title': 'Keyword Extractor', 'extracted_keywords': None}
    agent_slug = 'keyword-extractor'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        context['submitted_text'] = input_text
        if input_text:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Extract the 5-10 most relevant keywords or key phrases from the following text. Present them as a comma-separated list.

Text:
---
{input_text}
---

Keywords:"""
                    response = model.generate_content(prompt)
                    keywords_list = [kw.strip() for kw in response.text.strip().split(',') if kw.strip()]
                    context['extracted_keywords'] = keywords_list
                    messages.success(request, "Keywords extracted (Gemini AI)!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['extracted_keywords'] = ["Error extracting keywords."]
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['extracted_keywords'] = ["Placeholder Keyword 1", "Placeholder Keyword 2"]
        else:
            messages.error(request, "Please enter text to extract keywords from.")
            context['extracted_keywords'] = []
    return render(request, 'agentify/tools/keyword_extractor.html', context)

# Tool 8: Data Anonymizer
# @login_required
def data_anonymizer_view(request):
    """Handles the Data Anonymizer tool page, using Gemini AI (Use with Caution)."""
    context = {'page_title': 'Data Anonymizer', 'anonymized_data': None}
    agent_slug = 'data-anonymizer'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        input_data = request.POST.get('input_data', '').strip()
        context['submitted_data'] = input_data
        if input_data:
            if GEMINI_CONFIGURED and model:
                try:
                    # WARNING: AI-based anonymization is complex and may not be reliable.
                    # This prompt is a basic attempt and should not be used for sensitive production data without rigorous testing and potentially combining with rule-based methods.
                    prompt = f"""Analyze the following text and replace common types of Personally Identifiable Information (PII) such as names, email addresses, phone numbers, and potentially locations or specific IDs with generic placeholders like [NAME], [EMAIL], [PHONE], [LOCATION], [ID]. Be careful not to alter the structure significantly.

Original Text:
---
{input_data}
---

Anonymized Text:"""
                    response = model.generate_content(prompt)
                    context['anonymized_data'] = response.text
                    messages.success(request, "Data anonymization attempted (Gemini AI). Review carefully!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['anonymized_data'] = "Error during anonymization attempt."
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['anonymized_data'] = "[AI Service Not Configured - Placeholder Anonymized Data]"
        else:
            messages.error(request, "Please enter data to anonymize.")
            context['anonymized_data'] = ""
    return render(request, 'agentify/tools/data_anonymizer.html', context)

# Tool 9: Trend Spotter
# @login_required
def trend_spotter_view(request):
    """Handles the Trend Spotter tool page, using Gemini AI (Conceptual)."""
    context = {'page_title': 'Trend Spotter', 'trends': None}
    agent_slug = 'trend-spotter'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        data_source = request.POST.get('data_source', '').strip()
        context['submitted_source'] = data_source
        if data_source:
            if GEMINI_CONFIGURED and model:
                try:
                    # This is a complex task. The prompt needs to be carefully designed.
                    # Might need to specify timeframes, industries, etc.
                    prompt = f"""Analyze the following topic or data source description and identify 3-5 potential emerging trends related to it. List the trends clearly, one per line.

Topic/Source: {data_source}

Potential Trends:"""
                    response = model.generate_content(prompt)
                    context['trends'] = parse_ai_list_response(response.text)
                    messages.success(request, "Potential trends identified (Gemini AI).")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['trends'] = ["Error identifying trends."]
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['trends'] = ["[Placeholder Trend 1]", "[Placeholder Trend 2]"]
        else:
            messages.error(request, "Please specify a data source or topic.")
            context['trends'] = []
    # This tool likely needs more complex input/display than a simple form
    return render(request, 'agentify/tools/trend_spotter.html', context)

# Tool 10: Code Explainer
# @login_required
def code_explainer_view(request):
    """Handles the Code Explainer tool page, using Gemini AI."""
    context = {'page_title': 'Code Explainer', 'explanation': None}
    agent_slug = 'code-explainer'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        code_snippet = request.POST.get('code_snippet', '').strip()
        language = request.POST.get('language', 'python')
        context['submitted_code'] = code_snippet
        context['selected_language'] = language
        if code_snippet:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Explain the following {language} code snippet in simple terms. Describe its purpose, inputs, outputs, and main logic steps. Format the explanation clearly, potentially using Markdown.

                    Code Snippet:
                    ``` {language}
                    {code_snippet}
                    Explanation:"""
                    response = model.generate_content(prompt)
                    explanation_html = markdown.markdown(response.text, extensions=['extra', 'nl2br', 'sane_lists', 'fenced_code'])
                    context['explanation'] = explanation_html
                    messages.success(request, "Code explanation generated (Gemini AI).")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['explanation'] = "&lt;p>Error generating explanation.&lt;/p>"
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['explanation'] = "&lt;p>[AI Service Not Configured - Placeholder Explanation]&lt;/p>"
        else:
            messages.error(request, "Please enter a code snippet.")
            context['explanation'] = ""
    return render(request, 'agentify/tools/code_explainer.html', context)
        
@login_required
def regex_generator_view(request):
    """Handles the Regex Generator tool page, using Gemini AI."""
    context = {'page_title': 'Regex Generator', 'generated_regex': None}
    agent_slug = 'regex-generator'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        context['submitted_description'] = description
        if description:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Generate a Python-compatible regular expression pattern based on the following description. Provide only the regex pattern itself, without any surrounding text or explanation.
                    Description: {description}
                    Regex Pattern:"""
                    response = model.generate_content(prompt)
                    # Clean potential markdown code fences if AI adds them
                    regex_pattern = response.text.strip().strip('`')
                    context['generated_regex'] = regex_pattern
                    messages.success(request, "Regex pattern generated (Gemini AI)!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['generated_regex'] = "Error generating regex."
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['generated_regex'] = "[AI Service Not Configured]"
        else:
            messages.error(request, "Please describe the pattern you need.")
            context['generated_regex'] = ""
    return render(request, 'agentify/tools/regex_generator.html', context)

@login_required
def docstring_writer_view(request):
    """Handles the Docstring Writer tool page, using Gemini AI."""
    context = {'page_title': 'Docstring Writer', 'generated_docstring': None}
    agent_slug = 'docstring-writer'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        code_snippet = request.POST.get('code_snippet', '').strip()
        language = request.POST.get('language', 'python')
        context['submitted_code'] = code_snippet
        context['selected_language'] = language
        if code_snippet:
            if GEMINI_CONFIGURED and model:
                try:
                    # Adjust prompt based on language for common docstring formats
                    if language == 'python':
                        doc_format = 'Google style or reStructuredText'
                    elif language == 'javascript':
                        doc_format = 'JSDoc style'
                    else:
                        doc_format = 'a standard documentation comment style'

                    prompt = f"""Generate a {doc_format} docstring/comment for the following {language} function or class definition. Include descriptions for parameters and return values if applicable. Provide only the docstring/comment block itself.
                    Code:
                    ```{language}
                    {code_snippet}
                    Docstring/Comment:"""
                    response = model.generate_content(prompt)
                    # Clean potential markdown code fences
                    docstring = response.text.strip().strip('`')
                    context['generated_docstring'] = docstring
                    messages.success(request, "Docstring generated (Gemini AI)!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['generated_docstring'] = "# Error generating docstring."
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['generated_docstring'] = "[AI Service Not Configured - Placeholder Docstring]"
        else:
            messages.error(request, "Please enter a code snippet.")
            context['generated_docstring'] = ""
    return render(request, 'agentify/tools/docstring_writer.html', context)

@login_required
def api_request_formatter_view(request):
    """Handles the API Request Formatter tool page, using Gemini AI."""
    context = {'page_title': 'API Request Formatter', 'formatted_request': None}
    agent_slug = 'api-request-formatter'
    try: 
        context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: 
        context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        endpoint = request.POST.get('endpoint', '').strip()
        method = request.POST.get('method', 'GET')
        params = request.POST.get('params', '').strip() # Simple key=value pairs for now
        context['submitted_endpoint'] = endpoint
        context['selected_method'] = method
        context['submitted_params'] = params
        if endpoint:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Generate an example API request using curl based on the following details. Include common headers like Authorization (with a placeholder token) and Content-Type if appropriate for the method. Format query parameters correctly.
                    Method: {method}
                    Endpoint URL: {endpoint}
                    Query Parameters (one per line, key=value):
                    {params if params else 'None'}

                    Curl Example:"""
                    response = model.generate_content(prompt)
                    context['formatted_request'] = response.text.strip()
                    messages.success(request, "API request example formatted (Gemini AI)!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['formatted_request'] = "# Error formatting request."
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['formatted_request'] = "# [AI Service Not Configured - Placeholder Request]"
        else:
            messages.error(request, "Please enter an API endpoint URL.")
            context['formatted_request'] = ""
    return render(request, 'agentify/tools/api_request_formatter.html', context)

@login_required
def image_alt_text_generator_view(request):
    """Handles the Image Alt Text Generator tool page, using Gemini AI (Conceptual)."""
    context = {'page_title': 'Image Alt Text Generator', 'generated_alt_text': None}
    agent_slug = 'image-alt-text-generator'
    try: 
        context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: 
        context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")
    if request.method == 'POST':
        # NOTE: This currently only works with descriptions/URLs.
        # Actual image upload requires file handling and a multimodal model.
        image_input = request.POST.get('image_input', '').strip()
        context['submitted_input'] = image_input
        if image_input:
            if GEMINI_CONFIGURED and model:
                # Check if input looks like a URL, otherwise treat as description
                is_url = image_input.startswith('http://') or image_input.startswith('https://')
                input_type = "URL" if is_url else "description"

                # *** IMPORTANT: Gemini (text models like flash/pro) cannot directly process images from URLs or uploads via this library. ***
                # *** You would need a multimodal model (like gemini-1.5-pro) and use its specific image input capabilities. ***
                # *** This implementation will just use the URL/description as text input for a conceptual response. ***

                try:
                    prompt = f"""Generate concise and descriptive alt text for an image based on the following {input_type}:
                    Input: {image_input}

                    Alt Text:"""
                    response = model.generate_content(prompt)
                    context['generated_alt_text'] = response.text.strip()
                    messages.success(request, "Alt text generated (Gemini AI - based on text input).")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['generated_alt_text'] = "Error generating alt text."
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['generated_alt_text'] = "[AI Service Not Configured - Placeholder Alt Text]"
        else:
            messages.error(request, "Please provide an image URL or description.")
            context['generated_alt_text'] = ""
    return render(request, 'agentify/tools/image_alt_text_generator.html', context)

@login_required
def color_palette_suggester_view(request):
    """Handles the Color Palette Suggester tool page, using Gemini AI."""
    context = {'page_title': 'Color Palette Suggester', 'generated_palette': None}
    agent_slug = 'color-palette-suggester'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        base_input = request.POST.get('base_input', '').strip() # Could be color hex, description, or image URL
        context['submitted_input'] = base_input
        if base_input:
            if GEMINI_CONFIGURED and model:
                try:
                    # Ask for hex codes specifically
                    prompt = f"""Suggest a harmonious color palette of 5 colors (including the base, if applicable) based on the following input. Provide the colors as HEX codes, separated by commas.
                    Input: {base_input}

                    Color Palette (HEX codes, comma-separated):"""
                    response = model.generate_content(prompt)
                    # Basic parsing for hex codes
                    colors = re.findall(r'#[0-9a-fA-F]{6}', response.text)
                    # Fallback if regex fails but response exists
                    if not colors and response.text:
                        colors = [c.strip() for c in response.text.split(',') if c.strip().startswith('#')]
                        context['generated_palette'] = colors[:5] # Limit to 5
                        if colors:
                            messages.success(request, "Color palette suggested (Gemini AI)!")
                        else:
                            messages.warning(request, "Could not extract colors from AI response. Raw: " + response.text[:100])
                            context['generated_palette'] = []

                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['generated_palette'] = ["#Error"]
                else:
                    messages.warning(request, "AI service not configured. Showing placeholder.")
                    context['generated_palette'] = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#F1C40F"]
            else:
                messages.error(request, "Please provide a base color, description, or image URL.")
                context['generated_palette'] = []
    return render(request, 'agentify/tools/color_palette_suggester.html', context)

@login_required
def logo_idea_generator_view(request):
    """Handles the Basic Logo Idea Generator tool page, using Gemini AI."""
    context = {'page_title': 'Basic Logo Idea Generator', 'logo_ideas': None}
    agent_slug = 'basic-logo-idea-generator'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        company_name = request.POST.get('company_name', '').strip()
        industry = request.POST.get('industry', '').strip()
        context['submitted_company'] = company_name
        context['submitted_industry'] = industry
        if company_name and industry:
            if GEMINI_CONFIGURED and model:
                try:
                    prompt = f"""Generate 3-5 distinct conceptual ideas for a logo based on the company name and industry. Describe the concepts briefly (e.g., symbol, style, text treatment). Do not generate images, only text descriptions. Format as a simple list.

Company Name: {company_name}
Industry: {industry}

Logo Concepts:"""
                    response = model.generate_content(prompt)
                    context['logo_ideas'] = parse_ai_list_response(response.text)
                    messages.success(request, "Logo ideas generated (Gemini AI)!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['logo_ideas'] = ["Error generating ideas."]
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['logo_ideas'] = ["[Placeholder Logo Idea 1]", "[Placeholder Logo Idea 2]"]
        else:
            messages.error(request, "Please enter both company name and industry.")
            context['logo_ideas'] = []
    return render(request, 'agentify/tools/logo_idea_generator.html', context)

# Tool 17: Language Translator
# @login_required
def language_translator_view(request):
    """Handles the Language Translator tool page, using Gemini AI."""
    context = {'page_title': 'Language Translator', 'translated_text': None}
    agent_slug = 'language-translator'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    languages = {'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German', 'ja': 'Japanese', 'hi': 'Hindi'} # Added Hindi
    context['languages'] = languages

    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        source_lang_code = request.POST.get('source_lang', 'en')
        target_lang_code = request.POST.get('target_lang', 'es')
        context['submitted_text'] = input_text
        context['selected_source'] = source_lang_code
        context['selected_target'] = target_lang_code

        if input_text and source_lang_code != target_lang_code:
            if GEMINI_CONFIGURED and model:
                try:
                    source_lang_name = languages.get(source_lang_code, source_lang_code)
                    target_lang_name = languages.get(target_lang_code, target_lang_code)
                    prompt = f"""Translate the following text from {source_lang_name} to {target_lang_name}. Provide only the translated text.

Text to translate:
{input_text}

Translation:"""
                    response = model.generate_content(prompt)
                    context['translated_text'] = response.text.strip()
                    messages.success(request, f"Text translated to {target_lang_name} (Gemini AI)!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['translated_text'] = "Error during translation."
            else:
                 messages.warning(request, "AI service not configured. Showing placeholder.")
                 context['translated_text'] = "[AI Service Not Configured - Placeholder Translation]"
        elif source_lang_code == target_lang_code:
             messages.error(request, "Source and target languages cannot be the same.")
             context['translated_text'] = ""
        else:
            messages.error(request, "Please enter text to translate.")
            context['translated_text'] = ""
    return render(request, 'agentify/tools/language_translator.html', context)

# Tool 18: Grammar & Spell Checker
# @login_required
def grammar_checker_view(request):
    """Handles the Grammar & Spell Checker tool page, using Gemini AI."""
    context = {'page_title': 'Grammar & Spell Checker', 'checked_text': None, 'corrections': None}
    agent_slug = 'grammar-spell-checker'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        context['submitted_text'] = input_text
        if input_text:
            if GEMINI_CONFIGURED and model:
                try:
                    # Ask for both corrected text and a list of changes
                    prompt = f"""Please correct the grammar and spelling in the following text. Provide the corrected text first, followed by a blank line, and then a numbered list of the main changes made.

Original Text:
---
{input_text}
---

Corrected Text:
[Corrected text goes here]

Changes Made:
1. [Change 1]
2. [Change 2]
..."""
                    response = model.generate_content(prompt)
                    parts = response.text.split('Changes Made:', 1)
                    checked_text = parts[0].replace('Corrected Text:', '').strip()
                    corrections_list = []
                    if len(parts) > 1:
                        corrections_raw = parts[1].strip()
                        corrections_list = parse_ai_list_response(corrections_raw)

                    context['checked_text'] = checked_text
                    context['corrections'] = corrections_list
                    messages.success(request, "Grammar and spelling checked (Gemini AI)!")
                except Exception as e:
                    messages.error(request, f"AI Error: {e}")
                    context['checked_text'] = input_text # Return original on error
                    context['corrections'] = ["Error during check."]
            else:
                messages.warning(request, "AI service not configured. Showing placeholder.")
                context['checked_text'] = input_text + " [AI Service Not Configured]"
                context['corrections'] = ["Placeholder correction."]
        else:
            messages.error(request, "Please enter text to check.")
            context['checked_text'] = ""
            context['corrections'] = []
    return render(request, 'agentify/tools/grammar_checker.html', context)

# Tool 19: Unit Converter
# @login_required
def unit_converter_view(request):
    """
    Handles the Unit Converter tool page.
    NOTE: Unit conversion uses placeholder logic, NOT AI.
    """
    context = {'page_title': 'Unit Converter', 'converted_value': None}
    agent_slug = 'unit-converter'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")

    # Example units - A real app would need a comprehensive unit library
    units = {
        'length': {'m': 'Meters', 'km': 'Kilometers', 'mi': 'Miles', 'ft': 'Feet'},
        'temp': {'c': 'Celsius', 'f': 'Fahrenheit', 'k': 'Kelvin'},
        'mass': {'kg': 'Kilograms', 'lb': 'Pounds', 'g': 'Grams'}
        }
    context['unit_categories'] = units

    if request.method == 'POST':
        input_value_str = request.POST.get('input_value', '').strip()
        from_unit = request.POST.get('from_unit', '')
        to_unit = request.POST.get('to_unit', '')
        context.update({'submitted_value': input_value_str, 'selected_from': from_unit, 'selected_to': to_unit})

        try:
            value = float(input_value_str)
            if from_unit and to_unit and from_unit != to_unit:
                # --- !!! Placeholder Conversion Logic !!! ---
                result_value = None
                if from_unit == 'm' and to_unit == 'ft': result_value = value * 3.28084
                elif from_unit == 'ft' and to_unit == 'm': result_value = value / 3.28084
                elif from_unit == 'km' and to_unit == 'mi': result_value = value * 0.621371
                elif from_unit == 'mi' and to_unit == 'km': result_value = value / 0.621371
                elif from_unit == 'c' and to_unit == 'f': result_value = (value * 9/5) + 32
                elif from_unit == 'f' and to_unit == 'c': result_value = (value - 32) * 5/9
                elif from_unit == 'kg' and to_unit == 'lb': result_value = value * 2.20462
                elif from_unit == 'lb' and to_unit == 'kg': result_value = value / 2.20462
                # Add many more conversions...

                if result_value is not None:
                    # Try to find the category to get the full name, fallback to code
                    from_cat = next((cat for cat, u_dict in units.items() if from_unit in u_dict), None)
                    to_cat = next((cat for cat, u_dict in units.items() if to_unit in u_dict), None)
                    to_unit_name = units.get(to_cat, {}).get(to_unit, to_unit) if to_cat else to_unit

                    context['converted_value'] = f"{result_value:.4g} {to_unit_name}" # Format result
                    messages.success(request, "Conversion successful!")
                else:
                     messages.error(request, f"Conversion from '{from_unit}' to '{to_unit}' not supported yet.")
                     context['converted_value'] = ""
                 # --- End Placeholder Logic ---

            elif from_unit == to_unit:
                 messages.error(request, "'From' and 'To' units cannot be the same.")
                 context['converted_value'] = ""
            else:
                 messages.error(request, "Please select both 'From' and 'To' units.")
                 context['converted_value'] = ""
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid number to convert.")
            context['converted_value'] = ""

    return render(request, 'agentify/tools/unit_converter.html', context)

# Tool 20: Simple Q&A Bot (Already has Gemini Integration)
# @login_required
def simple_qa_bot_view(request):
    """Handles the Simple Q&A Bot tool page, using Gemini AI."""
    context = {'page_title': 'Simple Q&A Bot', 'answer': None}; agent_slug = 'simple-qa-bot'
    try: context['agent'] = Agent.objects.get(slug=agent_slug)
    except Agent.DoesNotExist: context['agent'] = None; messages.warning(request, f"Agent data for '{agent_slug}' not found.")
    if request.method == 'POST':
        context_text = request.POST.get('context_text', '').strip(); question = request.POST.get('question', '').strip()
        context.update({'submitted_context': context_text, 'submitted_question': question})
        if context_text and question:
            if GEMINI_CONFIGURED and model:
                try: prompt = f"Based ONLY on the following context, please answer the question. If the answer cannot be found in the context, say \"I cannot answer based on the provided context.\"\n\nContext:\n---\n{context_text}\n---\n\nQuestion: {question}\n\nAnswer:"; response = model.generate_content(prompt); context['answer'] = response.text; messages.success(request, "Answer generated (Gemini AI).")
                except Exception as e: messages.error(request, f"AI Error: {e}"); context['answer'] = "Error."
            else: messages.warning(request, "AI service not configured."); context['answer'] = "[Placeholder Answer]"
        else: messages.error(request, "Provide context and question."); context['answer'] = ""
    return render(request, 'agentify/tools/simple_qa_bot.html', context)