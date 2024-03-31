from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer

# Create your views here.
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
    user = serializer.save()
    return Response({
        'status': 'success',
        'data':{
            'id': user.id,
            'email': user.email,
            'phone': user.phone,
            'first_name': user.first_name,
            'last_name': user.last_name
        }})



from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

@api_view(['POST'])
def login(request):
    email_or_phone = request.data.get('email_phone')
    password = request.data.get('password')
    if email_or_phone is None or password is None:
        return Response({"message": "Email/phone và password là bắt buộc."}, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(email_or_phone, int):
        try:
            user = User.objects.get(phone=email_or_phone)
        except User.DoesNotExist:
            return Response({"message": "Thông tin đăng nhập không hợp lệ."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            user = User.objects.get(email=email_or_phone)
        except User.DoesNotExist:
            return Response({"message": "Thông tin đăng nhập không hợp lệ."}, status=status.HTTP_401_UNAUTHORIZED)
    if user.password!=password:
        return Response({"message": "Thông tin đăng nhập không hợp lệ."}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'email': user.email,
            'phone': user.phone,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    })



