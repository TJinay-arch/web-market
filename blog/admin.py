from django.contrib import admin

from .models import Records


@admin.register(Records)
class RecordsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_filter = ("created_at",)
    search_fields = (
        "name",
        "created_at",
    )
