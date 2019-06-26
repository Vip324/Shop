from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name = 'Age', default=18)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expire = models.DateTimeField(default=(timezone.now() + timezone.timedelta(hours=48)))

    def is_activation_key_expire(self):
        return timezone.now() > self.activation_key_expire

    email = models.EmailField(unique=True)

class ShopUserProfile(models . Model):
    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name = 'Tagline', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name = 'AboutMe', max_length=512, blank=True)

    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        ( MALE , 'М'),
        ( FEMALE , 'Ж'),
    )
    gender = models.CharField(verbose_name ='Sex', max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, ** kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, ** kwargs):
        instance.shopuserprofile.save()