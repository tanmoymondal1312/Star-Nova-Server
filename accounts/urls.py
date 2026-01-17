from django.urls import path
from .views import login, varify_number

urlpatterns = [
    path('api/login', login, name='login'),
    path('api/verify-number', varify_number, name='verify_number'),
    #path('api/get-set-user-data', get_and_set_user_data, name='get_and_set_user_data'),
]
