import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save


NULLABLE = {'blank': True, 'null': True}


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users', blank=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Возраст')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expired = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) <= self.activation_key_expired + timedelta(hours=48):
            return False
        return True


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'

    GENDERS = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (UNKNOWN, 'Н'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)

    tagline = models.CharField(max_length=128, **NULLABLE, verbose_name='Тэги')
    about_me = models.TextField(max_length=512, **NULLABLE, verbose_name='Обо мне')
    gender = models.CharField(choices=GENDERS, default=UNKNOWN, max_length=1, verbose_name='Пол')

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()


