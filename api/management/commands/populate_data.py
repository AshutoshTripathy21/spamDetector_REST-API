from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from api.models import User, Contact

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample users
        user1 = User.objects.create(name='User1', phone_number='1234567890', password=make_password('password'))
        user2 = User.objects.create(name='User2', phone_number='9876543210', password=make_password('password'))

        # Add sample contacts for users
        Contact.objects.create(user=user1, name='Contact1', phone_number='1111111111')
        Contact.objects.create(user=user1, name='Contact2', phone_number='2222222222')
        Contact.objects.create(user=user2, name='Contact3', phone_number='3333333333')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully'))
