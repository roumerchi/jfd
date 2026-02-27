from django.core.management import BaseCommand

from contacts.models import Contacts, ContactStatus, CustomUser


class Command(BaseCommand): # had to be created to fill in the default values for ContactStatus model
    """fills db with the necessary basic data"""
    help = "initialization command, run this command once"

    def handle(self, *args, **options):
        if self.is_data_initialized():
            self.stdout.write(self.style.ERROR('Initial data has already been initialized'))
        else:
            self.stdout.write(self.style.NOTICE('Initialization...'))

            generate_data()

            self.stdout.write(self.style.SUCCESS('Initialization completed'))

    @staticmethod
    def is_data_initialized():
        return ContactStatus.objects.filter(code='default').exists()

def generate_data():
    default_status = ContactStatus.objects.create(
        code='default', title='Default', is_active=True
    )
    ContactStatus.objects.create(
        code='blocked', title='Blocked', is_active=True
    )

    if not CustomUser.objects.filter(username='admin').exists():
        user = CustomUser.objects.create_superuser(username='admin', email='admin@example.com', password='root')
    else:
        user = CustomUser.objects.create(username='user', email='user@example.com', password='user')

    Contacts.objects.create(
        owner=user,
        first_name='Test_User',
        last_name='First',
        phone='+48123123123',
        email='test.user@example.com',
        city='Wroclaw',
        status=default_status
    )
