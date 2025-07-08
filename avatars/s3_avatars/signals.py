from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserProfile
from .utils import process_avatar


@receiver(pre_save, sender=UserProfile)
def avatar_process_signal(sender, instance, *kwargs):
    if instance.avatar and not getattr(instance, '_avatar_processed', False):
        instance.avatar = process_avatar(instance.avatar)
        instance._avatar_processed = True
