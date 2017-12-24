from django.contrib import admin

from .models import Feedback



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author', 'work_at', 'is_active')
    list_editable = ('is_active',)
    list_filter = ['is_active']
    search_fields = ['author']
