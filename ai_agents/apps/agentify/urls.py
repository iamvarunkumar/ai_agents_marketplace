# E:\Projects\AI Agents\ai_agents\apps\agentify\urls.py

from django.urls import path
# Import views from *this* app's views.py file
from . import views

# Namespace for agentify-related URLs (used in {% url 'agentify:...' %} tags)
app_name = 'agentify'

urlpatterns = [
    # URL for listing agents
    path('', views.BasicAgentListView.as_view(), name='agent_list_basic'),
    path('pro/', views.ProAgentListView.as_view(), name='agent_list_pro'),
    path('advanced/', views.AdvancedAgentListView.as_view(), name='agent_list_advanced'),
# ... other tool/detail paths ...


    # --- Tool-Specific URLs ---
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
    # ADDED: URLs for remaining 5 tools
    path('tools/logo-idea-generator/', views.logo_idea_generator_view, name='logo_idea_generator'),
    path('tools/language-translator/', views.language_translator_view, name='language_translator'),
    path('tools/grammar-checker/', views.grammar_checker_view, name='grammar_checker'),
    path('tools/unit-converter/', views.unit_converter_view, name='unit_converter'),
    path('tools/simple-qa-bot/', views.simple_qa_bot_view, name='simple_qa_bot'),
    
    # 
    path('tools_advanced/article-summarizer/', views.article_summarizer_view, name='article_summarizer'),
    path('tools_advanced/meeting-notes-bot/', views.meeting_notes_bot_view, name='meeting_notes_bot'),
    path('tools_advanced/document-digest/', views.document_digest_view, name='document_digest'),
    path('tools_advanced/ad-copy-generator/', views.ad_copy_generator_view, name='ad_copy_generator'),
    path('tools_advanced/email-reply-bot/', views.email_reply_bot_view, name='email_reply_bot'),
    path('tools_advanced/draft-chat-reply-bot/', views.chat_reply_draft_view, name='draft_chat_reply_bot'),
    path('tools_advanced/social-media-reply-bot/', views.social_media_reply_bot_view, name='social_media_reply_bot'),
    path('tools_advanced/technical-term-explainer/', views.tech_term_explainer_view, name='technical_term_explainer'),
    path('tools_advanced/code-explanation-bot/', views.code_explanation_bot_view, name='code_explanation_bot'),
    path('tools_advanced/concept-explainer/', views.concept_explainer_view, name='concept_explainer'),
    path('tools_advanced/user-management-bot/', views.user_management_bot_view, name='user_management_bot'),
    path('tools_advanced/data-backup-bot/', views.data_backup_bot_view, name='data_backup_bot'),
    path('tools_advanced/performance-monitoring-bot/', views.performance_monitoring_bot_view, name='performance_monitoring_bot'),
    path('tools_advanced/email-notification-bot/', views.email_notification_bot_view, name='email_notification_bot'),
    path('tools_advanced/form-submission-bot/', views.form_submission_bot_view, name='form_submission_bot'),
    path('tools_advanced/search-optimization-bot/', views.search_optimization_bot_view, name='search_optimization_bot'),
    path('tools_advanced/data-entry-bot/', views.data_entry_bot_view, name='data_entry_bot'),
    path('tools_advanced/scheduling-bot/', views.scheduling_bot_view, name='scheduling_bot'),
    path('tools_advanced/reminder-bot/', views.reminder_bot_view, name='reminder_bot'),
    path('tools_advanced/personalization-bot/', views.personalization_bot_view, name='personalization_bot'),
    

    # --- Agent Detail & Workspace URLs ---
    path('<slug:slug>/', views.AgentDetailView.as_view(), name='agent_detail'),
    path('<slug:agent_slug>/add/', views.add_to_workspace, name='add_to_workspace'),
    path('<slug:agent_slug>/remove/', views.remove_from_workspace, name='remove_from_workspace'),

]