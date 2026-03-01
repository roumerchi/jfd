from django.core.management import BaseCommand

from contacts.models import Contacts, ContactStatus, CustomUser
from supra.settings import DEBUG


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
    default_status = ContactStatus.objects.create(code='default', title='Default', is_active=True)
    ContactStatus.objects.create(code='blocked', title='Blocked', is_active=True)

    if DEBUG:
        generate_additional_data(default_status)

def generate_additional_data(default_status):
    if not CustomUser.objects.filter(username='admin').exists():
        user = CustomUser.objects.create_superuser(username='admin', email='admin@example.com', password='root')
    else:
        user = CustomUser.objects.create(username='user', email='user@example.com', password='user')

    polish_cities = [
        "Warsaw", "Krakow", "Lodz", "Wroclaw", "Poznan", "Gdansk",
        "Szczecin", "Bydgoszcz", "Lublin", "Bialystok", "Katowice"
    ]
    contacts_to_create = []
    for i in range(11):
        contacts_to_create.append(
            Contacts(
                owner=user,
                first_name=f'Test_User_{i}',
                last_name=f'Number_{i:02d}',
                phone=f'+481234000{i:02d}',
                email=f'user{i}@example.com',
                city=polish_cities[i],
                status=default_status
            )
        )
    Contacts.objects.bulk_create(contacts_to_create)
