from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    ChangePasswordView,
    UserAvatarUploadView,
    AvatarListView,
    AvatarDetailView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('upload-avatar/', UserAvatarUploadView.as_view(), name='upload-avatar'),
    path('avatars/', AvatarListView.as_view(), name='avatars-list'),
    path('avatars/<int:pk>/', AvatarDetailView.as_view(), name='avatars-detail'),
]
