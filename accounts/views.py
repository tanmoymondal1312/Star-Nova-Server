import random
import string
from django.contrib.auth.models import User
from .models import UserData
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

def generate_random_password(length=8):
    """Generate a random password with letters and digits"""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def generate_temporary_username():
    """Generate a unique temporary username"""
    prefix = "user_"
    suffix = ''.join(random.choice(string.digits) for _ in range(6))
    return prefix + suffix

@api_view(['POST'])
def login(request):
    data = request.data
    phone = data.get('phone')

    if not phone:
        return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

    user_created = False
    password = None
    
    # Check if there's any UserData with this phone number
    try:
        # Try to find existing user with this phone number
        user_data = UserData.objects.get(mobile_number=phone)
        user = user_data.user
        password = "Already set"
    except UserData.DoesNotExist:
        # Create new user with temporary username
        username = generate_temporary_username()
        
        # Ensure username is unique
        while User.objects.filter(username=username).exists():
            username = generate_temporary_username()
        
        password = generate_random_password()
        user = User.objects.create_user(username=username, password=password)
        
        # Create UserData with the phone number
        UserData.objects.create(user=user, mobile_number=phone, is_paid=False)
        user_created = True

    # Get or create token
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "username": user.username,
        "password": password if user_created else "Already set",
        "phone": phone
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
def varify_number(request):
    data = request.data
    phone = data.get('phone')

    if not phone:
        return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=phone)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "Number verified successfully", "token": token.key}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)