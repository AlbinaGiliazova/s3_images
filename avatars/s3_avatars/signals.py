from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserProfile
from .utils import process_avatar


@receiver(pre_save, sender=UserProfile)
def process_avatar_before_save(sender, instance, *kwargs):
    if (
        instance.avatar
        and hasattr(instance.avatar, 'file')
        and not hasattr(instance.avatar.file, 'was_processed')
    ):
        # Защита, чтобы обработка не происходила повторно на каждом save
        # Перемотка на начало файла
        instance.avatar.file.seek(0)
        processed = process_avatar(instance.avatar.file)
        # Ставим флаг во избежание повторной обработки
        processed.file.was_processed = True
        instance.avatar = processed
