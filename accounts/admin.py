from django.contrib import admin
from .models import UserData

from django.contrib import admin
from .models import UserData


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'language',
        'experience_level',
        'is_paid'
    )
