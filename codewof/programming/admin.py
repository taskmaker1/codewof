"""Admin configuration for programming."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from programming.models import Attempt, QuestionTypeDebugging

User = get_user_model()


class AttemptAdmin(admin.ModelAdmin):
    """Configuration for displaying attempts in admin."""

    list_display = ('datetime', 'question', 'profile', 'passed_tests')
    ordering = ('-datetime', )


admin.site.register(Attempt, AttemptAdmin)
admin.site.register(QuestionTypeDebugging)
