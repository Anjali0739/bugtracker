from django.contrib import admin
from .models import Bug
# Register your models here.

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'status', 'created_by', 'created_at')
    list_filter=('status',)
    search_fields=('title', 'description', 'created_by')

