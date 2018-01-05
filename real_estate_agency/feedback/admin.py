from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline

from .models import Feedback, SocialLinkForFeedback


class SocialLinkForFeedbackInline(admin.StackedInline):
    model = SocialLinkForFeedback
    extra = 1
    fields = ('link_type',
              'url',
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author', 'work_at', 'is_active')
    list_editable = ('is_active',)
    list_filter = ['is_active']
    search_fields = ['author']
    inlines = [SocialLinkForFeedbackInline]
