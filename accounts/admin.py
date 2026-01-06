from django.contrib import admin
from .models import UserData

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number', 'is_paid')
    search_fields = ('user__username', 'mobile_number')
    list_filter = ('is_paid',)
