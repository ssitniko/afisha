from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_401_UNAUTHORIZED

from .serializers import UserRegisterSerializer, UserAuthSerializer, UserConfirmationCode
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random


# Create your views here.
@api_view(['POST'])
def register_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username, password=password, is_active=False)
    code = str(random.randint(100000, 999999))
    UserConfirmationCode.objects.create(user=user, code=code)
    return Response({'message': 'User created. Confirm with the code.', 'code': code}, status=status.HTTP_201_CREATED)
    # return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id})


@api_view(['POST'])
def confirm_api_view(request):
    user_id = request.data.get('user_id')
    code = request.data.get('code')

    try:
        confirmation = UserConfirmationCode.objects.get(user_id=user_id, code=code)
    except UserConfirmationCode.DoesNotExist:
        return Response({'error': 'code or user is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

    user = confirmation.user
    user.is_active = True
    user.save()

    # confirmation.delete()
    return Response({'message': 'User has been confirmed!'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def auth_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})

    return Response(status=HTTP_401_UNAUTHORIZED, data={'User credentials are wrong!'})