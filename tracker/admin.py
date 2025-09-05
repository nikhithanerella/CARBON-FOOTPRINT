

# tracker/admin.py
from django.contrib import admin
from .models import UserProfile, FootprintEntry

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_footprint')

@admin.register(FootprintEntry)
class FootprintEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'prediction', 'created_at')
