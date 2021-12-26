import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.urls import reverse


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Возраст')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(blank=True, null=True)

    def safe_delete(self):
        self.is_active = False
        self.save()

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) < self.activation_key_expires:
            return False
        return True

    def send_verify_mail(self):
        verify_link = reverse('users:verify', args=[self.email, self.activation_key])
        subject = 'Account verify'
        message = f'{settings.BASE_URL}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)

    def verify(self, email, activation_key):
        if self.email == email and self.activation_key == activation_key and not self.is_activation_key_expired():
            self.is_active = True
            self.activation_key = None
            self.activation_key_expires = None
            self.save()
            return True
        return False


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'

    GENDERS = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
        (UNKNOWN, 'Не указан'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)

    tagline = models.CharField(max_length=128, blank=True, null=True, verbose_name='Тэги')
    about_me = models.CharField(max_length=512, blank=True, null=True, verbose_name='Обо мне')
    gender = models.CharField(choices=GENDERS, default=UNKNOWN, max_length=1, verbose_name='Пол')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance).save()
