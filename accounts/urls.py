from django.urls import path
from .views import login, varify_number

urlpatterns = [
    path('api/login', login, name='login'),
    path('api/verify-number', varify_number, name='verify_number'),
]
