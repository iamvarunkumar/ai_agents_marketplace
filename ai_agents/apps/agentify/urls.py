# E:\Projects\AI Agents\ai_agents\apps\agentify\urls.py

from django.urls import path
# Import views from *this* app when you create them
from . import views
from django.contrib import admin

app_name = 'agentify' # Namespace for agentify-related URLs

urlpatterns = [
    # Add URLs specific to the agentify app here later
    # Example:
    # path('', views.agent_list_view, name='agent_list'),
    # path('create/', views.agent_create_view, name='agent_create'),
    # path('<int:pk>/', views.agent_detail_view, name='agent_detail'),
    path('agents/', views.AgentListView.as_view(), name='agent_list'),
    path('<slug:slug>/', views.AgentDetailView.as_view(), name='agent_detail'),
    path('<slug:agent_slug>/remove/', views.remove_from_workspace, name='remove_from_workspace'),
    path('tools/blog-idea-generator/', views.blog_idea_generator_view, name='blog_idea_generator'),
    path('tools/product-description-writer/', views.product_description_writer_view, name='product_description_writer'),
    path('tools/social-media-post-creator/', views.social_media_post_creator_view, name='social_media_post_creator'),
    path('tools/email-subject-generator/', views.email_subject_generator_view, name='email_subject_generator'),
    path('tools/meeting-summarizer/', views.meeting_summarizer_view, name='meeting_summarizer'),
    path('tools/sentiment-analysis/', views.sentiment_analysis_view, name='sentiment_analysis'),
    path('tools/keyword-extractor/', views.keyword_extractor_view, name='keyword_extractor'),
    path('tools/data-anonymizer/', views.data_anonymizer_view, name='data_anonymizer'),
    path('tools/trend-spotter/', views.trend_spotter_view, name='trend_spotter'),
    path('tools/code-explainer/', views.code_explainer_view, name='code_explainer'),
    path('tools/regex-generator/', views.regex_generator_view, name='regex_generator'),
    path('tools/docstring-writer/', views.docstring_writer_view, name='docstring_writer'),
    path('tools/api-request-formatter/', views.api_request_formatter_view, name='api_request_formatter'),
    path('tools/image-alt-text-generator/', views.image_alt_text_generator_view, name='image_alt_text_generator'),
    path('tools/color-palette-suggester/', views.color_palette_suggester_view, name='color_palette_suggester'),
    path('tools/logo-idea-generator/', views.logo_idea_generator_view, name='logo_idea_generator'),
    path('tools/language-translator/', views.language_translator_view, name='language_translator'),
    path('tools/grammar-checker/', views.grammar_checker_view, name='grammar_checker'),
    path('tools/unit-converter/', views.unit_converter_view, name='unit_converter'),
    path('tools/simple-qa-bot/', views.simple_qa_bot_view, name='simple_qa_bot'),



]
