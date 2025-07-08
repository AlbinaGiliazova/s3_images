from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage

from .utils import process_avatar


# Модель профиля пользователя с аватаром
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='user_avatars/',
        null=True,
        blank=True,
        storage=S3Boto3Storage(),
    )

    def __str__(self):
        return f'Profile: {self.user.username}'

    def save(self, *args, **kwargs):
        if self.avatar and not getattr(self, 'avatar_processed', False):
            processed_file = process_avatar(self.avatar)
            self.avatar.save(
                processed_file.name,
                processed_file,
                save=False,  # не вызывать save() рекурсивно
            )
            self.avatar_processed = True
        super().save(*args, **kwargs)
