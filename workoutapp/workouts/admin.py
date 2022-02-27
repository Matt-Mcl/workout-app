from django.contrib import admin

from .models import Walk, Run


@admin.register(Walk)
class WalkAdmin(admin.ModelAdmin):
    list_display = ['location', 'duration', 'distance']

@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ['location', 'duration', 'distance']

