from django.core.management.base import BaseCommand

from users.models import User, UserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.all():
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)
