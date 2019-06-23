from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name = 'Age' )

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expire = models.DateTimeField(default=(timezone.now() + timezone.timedelta(hours=48)))

    def is_activation_key_expire(self):
        return timezone.now() > self.activation_key_expire