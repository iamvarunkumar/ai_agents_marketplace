from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
class Agent(models.Model):
    """
    Represents an AI Agent available in the marketplace.
    """
    # --- Tier Choices ---
    TIER_BASIC = 'basic'
    TIER_PRO = 'pro'
    TIER_ADVANCED = 'advanced'
    TIER_CHOICES = [
        (TIER_BASIC, 'Basic'),
        (TIER_PRO, 'Pro'),
        (TIER_ADVANCED, 'Advanced'),
    ]
    

    # --- Category Choices (Based on user list) ---
    CAT_CONTENT = 'content_creation'
    CAT_COMMUNICATION = 'communication'
    CAT_AUTOMATION = 'automation'
    CAT_ECOMMERCE = 'ecommerce'
    CAT_TRAVEL = 'travel'
    CAT_FITNESS = 'fitness_wellness'
    CAT_EDUCATION = 'education_learning'
    CAT_FINANCE = 'finance_investing'
    CAT_HOME = 'home_lifestyle'
    CAT_ENTERTAINMENT = 'entertainment'
    CAT_HEALTHCARE = 'healthcare'
    CAT_LEGAL = 'legal'
    CAT_REALESTATE = 'real_estate'
    CAT_BUSINESS = 'business'
    CAT_HR = 'human_resources'
    CAT_MARKETING = 'marketing'
    CAT_OTHER = 'other' # Fallback

    CATEGORY_CHOICES = [
        (CAT_CONTENT, 'Content Creation'),
        (CAT_COMMUNICATION, 'Communication'),
        (CAT_AUTOMATION, 'Automation'),
        (CAT_ECOMMERCE, 'E-commerce'),
        (CAT_TRAVEL, 'Travel'),
        (CAT_FITNESS, 'Fitness & Wellness'),
        (CAT_EDUCATION, 'Education & Learning'),
        (CAT_FINANCE, 'Finance & Investing'),
        (CAT_HOME, 'Home & Lifestyle'),
        (CAT_ENTERTAINMENT, 'Entertainment'),
        (CAT_HEALTHCARE, 'Healthcare'),
        (CAT_LEGAL, 'Legal'),
        (CAT_REALESTATE, 'Real Estate'),
        (CAT_BUSINESS, 'Business'),
        (CAT_HR, 'Human Resources'),
        (CAT_MARKETING, 'Marketing'),
        (CAT_OTHER, 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True, help_text="The unique name of the AI agent.")
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text="URL-friendly version of the name, auto-generated if left blank.")
    description = models.TextField(blank=True, help_text="A detailed description of what the agent does.")
    short_description = models.CharField(max_length=255, blank=True, help_text="A brief summary shown in list views.")
    # tier = models.CharField(max_length=20, choices=TIER_CHOICES, default=TIER_BASIC, help_text="Access tier for this agent.")
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default=TIER_BASIC, help_text="Access tier for this agent.")
    # ADDED: Category field
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=CAT_OTHER,
        help_text="The category this agent belongs to."
    )
    illustration = models.CharField(max_length=100, blank=True, null=True, help_text="Filename of the illustration in static/images/ (e.g., 'tool_icon.png')")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_agents', help_text="The user who created this agent.")
    is_public = models.BooleanField(default=True, help_text="Is this agent visible to everyone in the marketplace?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name'] # Order by category, then name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Generate tool-specific URL or fallback to detail view
        tool_url_name = f'agentify:{self.slug.replace("-", "_")}'
        try:
            return reverse(tool_url_name)
        except Exception:
            try:
                return reverse('agentify:agent_detail', kwargs={'slug': self.slug})
            except Exception:
                return "#"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)