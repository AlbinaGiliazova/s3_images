from django.apps import AppConfig


class S3AvatarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 's3_avatars'

    def ready(self):
        pass
