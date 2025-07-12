from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from s3_avatars.models import CustomUser
from s3_avatars.utils import process_avatar


class Avatar(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name=CustomUser._meta.verbose_name,
        related_name='avatars',
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(
        upload_to='user_avatars/',
        null=True,
        blank=True,
        storage=S3Boto3Storage(),
    )

    def __str__(self):
        return f'Avatar: {self.id}'

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
