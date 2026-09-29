from django.contrib import admin
from .models import Question, TestSession, UserAnswer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "difficulty", "correct_index", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("question_text",)
    ordering = ("order",)


@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ("uuid", "language", "status", "iq_score", "percentile", "started_at")
    list_filter = ("status", "language")
    readonly_fields = ("uuid", "started_at", "finished_at")


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("session", "question", "selected_index", "is_correct", "time_spent")
    list_filter = ("is_correct",)