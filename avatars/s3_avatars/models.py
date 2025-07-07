from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage


# Кастомное хранилище для S3
class MediaRootS3BotoStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


# Модель профиля пользователя с аватаром
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/', storage=MediaRootS3BotoStorage(), null=True, blank=True
    )

    def __str__(self):
        return f'Profile: {self.user.username}'
