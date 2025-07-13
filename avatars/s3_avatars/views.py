from rest_framework import generics, permissions, parsers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser, Avatar
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    AvatarSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (
        AllowAny,
    )  # Позволяет регистрироваться незалогиненным пользователям


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = self.get_object()
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': 'Wrong password.'}, status=400)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'Password updated'})
        return Response(serializer.errors, status=400)


class UserAvatarUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, *args, **kwargs):
        # Привязываем аватар строго к себе
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = AvatarSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvatarListView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]  # Можно только IsAuthenticated, если нужно

    def get(self, request):
        user_id = request.query_params.get('user')
        if user_id:
            avatars = Avatar.objects.filter(user_id=user_id)
        else:
            avatars = Avatar.objects.all()
        serializer = AvatarSerializer(avatars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvatarDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        serializer = AvatarSerializer(avatar)
        return Response(serializer.data, status=status.HTTP_200_OK)
