from django.contrib import admin

# Register your models here.
# matches/admin.py
from django.contrib import admin
from .models import Evaluation, Match

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("evaluator", "target", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("evaluator__username", "target__username")
    autocomplete_fields = ("evaluator", "target")

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("user1", "user2", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("user1__username", "user2__username")
    autocomplete_fields = ("user1", "user2")
