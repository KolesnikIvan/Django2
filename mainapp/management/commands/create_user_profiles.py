from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from authapp.models import ShopUserProfile

class Command(BaseCommand):
    # command to create user_profile, if user has no profile
    def handle(self, *args, **options):
        users =ShopUser.objects.all()
        for user in users:
            if not len(ShopUserProfile.objects.filter(user=user)):
                user_profile = ShopUserProfile.objects.create(user=user)
                user_profile.save()
