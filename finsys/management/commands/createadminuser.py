from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Add data from JSON'

    def create_superuser(self):
        user = get_user_model()
        if not user.objects.filter(username='root').exists():
            user.objects.create_superuser(username='root', password='root')
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: root'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "root" already exists'))
