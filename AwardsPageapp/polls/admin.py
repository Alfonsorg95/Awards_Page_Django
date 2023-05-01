from django.contrib import admin
from .models import Question, Choice


class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ["publication_date", "question_text"]
    inlines = [ChoiceInLine]
    list_display = ("question_text", "publication_date", "was_published_recently")
    list_filter = ["publication_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
