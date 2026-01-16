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
    


@api_view(['POST'])
def get_and_set_user_data(request):
    # 1️⃣ Get token from header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

    # Expected format: "Token <token>"
    try:
        token_key = auth_header.replace("Token ", "").strip()
    except IndexError:
        return Response({"error": "Invalid token format"}, status=status.HTTP_401_UNAUTHORIZED)

    # 2️⃣ Find user from token
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    # 3️⃣ Get or create user data
    user_data, created = UserData.objects.get_or_create(user=user)

    # 4️⃣ Update fields if provided
    data = request.data
    if 'language' in data:
        user_data.language = data['language']
    if 'name' in data:
        user_data.name = data['name']
    if 'experience_level' in data:
        user_data.experience_level = data['experience_level']
    if 'age' in data:
        try:
            age = int(data['age'])
            if age < 1 or age > 120:
                return Response({"error": "Invalid age"}, status=status.HTTP_400_BAD_REQUEST)
            user_data.age = age
        except (TypeError, ValueError):
            return Response({"error": "Age must be a number"}, status=status.HTTP_400_BAD_REQUEST)
    if 'classification' in data:
        user_data.classification = data['classification']
    user_data.mobile_number = user.phone 
    user_data.save()

    # 5️⃣ Return JSON response
    return Response({
        "message": "User data updated successfully",
        "user_data": {
            "language": user_data.language,
            "name": getattr(user_data, "name", ""),
            "experience_level": user_data.experience_level,
            "age": user_data.age,
            "classification": user_data.classification,
        }
    }, status=status.HTTP_200_OK)