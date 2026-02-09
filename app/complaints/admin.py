from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_by", "created_at","urgency_score")
    list_filter = ("category", "status")
    search_fields = ("title", "description")
