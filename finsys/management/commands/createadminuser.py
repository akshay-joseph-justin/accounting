from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Add data from JSON'

    def handle(self, *args, **kwargs):
        self.create_superuser()

    def create_superuser(self):
        user = get_user_model()
        if not user.objects.filter(username='root').exists():
            user.objects.create_superuser(username='root', password='root')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser: root'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "root" already exists'))
