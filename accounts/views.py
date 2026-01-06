import random
import string
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserData

def generate_random_password(length=8):
    """Generate a random password with letters and digits"""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

@api_view(['POST'])
def login(request):
    data = request.data
    phone = data.get('phone')

    if not phone:
        return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user exists
    user_created = False
    try:
        user = User.objects.get(username=phone)
        # User exists, no need to authenticate with password
        password = None
    except User.DoesNotExist:
        # User doesn't exist → create new
        password = generate_random_password()
        user = User.objects.create_user(username=phone, password=password)
        UserData.objects.create(user=user, mobile_number=phone, is_paid=False)
        user_created = True

    # Get or create token
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "name": user.username,
        "password": password if user_created else "Already set"  # Show password only if newly created
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