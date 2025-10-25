from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer
from .models import User



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            "message": "User registered successfully",
            "tokens": tokens,
            "full_name": user.full_name or user.email
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     serializer = LoginSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.validated_data['user']  # Make sure your serializer returns the user instance
#         tokens = get_tokens_for_user(user)
#         return Response({
#             "message": "Login successful",
#             "tokens": tokens,
#             "full_name": user.full_name or user.email
#         }, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']  # Make sure your serializer returns the user instance
        tokens = get_tokens_for_user(user)
        
        # Return tokens, full name, and email
        return Response({
            "message": "Login successful",
            "tokens": tokens,
            "full_name": user.full_name or f"{user.first_name} {user.last_name}" or user.email,
            "email": user.email  # <-- Add email here
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def current_user_view(request):
#     """
#     Returns the logged-in user's full name.
#     """
#     user = request.user
#     return Response({
#         "full_name": user.full_name or user.email
#     })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Returns the logged-in user's profile details.
    """
    user = request.user
    return Response({
        "id": user.id,
        "full_name": user.full_name or "",
        "email": user.email,
    })