from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from src.users.models import Profile
from src.users.serializers import ProfileSerializer
from django.utils import timezone
from datetime import timedelta
import random
from faker import Faker
import string
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with users and profiles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='The number of users to create'
        )
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete existing users before seeding'
        )
        parser.add_argument(
            '--admin',
            action='store_true',
            help='Create admin users'
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write('Flushing existing users and profiles...')
            Profile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        num_users = options['users']
        create_admin = options['admin']

        self.stdout.write(f'Starting to seed {num_users} users...')

        if create_admin:
            self.create_admin_users()

        self.create_regular_users(num_users)

        self.stdout.write(self.style.SUCCESS('Successfully seeded users and profiles'))

    def generate_numeric_username(self):
        """Generate a unique numeric username between 7-10 digits"""
        while True:
            # Generate a random number between 7 and 10 digits
            length = random.randint(7, 10)
            # Ensure first digit is not 0
            username = str(random.randint(1, 9))
            # Add remaining digits
            username += ''.join(str(random.randint(0, 9)) for _ in range(length - 1))

            # Check if username already exists
            if not User.objects.filter(username=username).exists():
                return username

    @transaction.atomic
    def create_admin_users(self):
        self.stdout.write('Creating admin users...')

        admin_users = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'adminpass123',
                'first_name': 'Admin',
                'last_name': 'User',
            },
            {
                'username': 'supervisor',
                'email': 'supervisor@example.com',
                'password': 'superpass123',
                'first_name': 'Super',
                'last_name': 'Visor',
            }
        ]

        for admin_data in admin_users:
            try:
                with transaction.atomic():
                    user, created = User.objects.get_or_create(
                        username=admin_data['username'],
                        defaults={
                            'email': admin_data['email'],
                            'first_name': admin_data['first_name'],
                            'last_name': admin_data['last_name'],
                            'is_staff': True,
                            'is_superuser': True,
                        }
                    )

                    if created:
                        user.set_password(admin_data['password'])
                        user.is_active = True
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()

                        # Update the automatically created profile
                        self.update_profile(user)
                        self.stdout.write(f'Created admin user: {user.username}')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating admin user {admin_data["username"]}: {str(e)}')
                )

    @transaction.atomic
    def create_regular_users(self, num_users):
        fake = Faker(['es_MX'])

        for i in range(num_users):
            try:
                with transaction.atomic():
                    # Generate user data
                    first_name = fake.first_name()
                    last_name = fake.last_name()
                    last_name2 = fake.last_name()
                    username = self.generate_numeric_username()
                    email = f"{username}@example.com"

                    # Create user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=self.generate_secure_password(),
                        first_name=first_name,
                        last_name=last_name,
                        last_name2=last_name2
                    )

                    # Update the automatically created profile
                    self.update_profile(user)
                    self.stdout.write(f'Created user and updated profile: {username}')

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating user {i + 1}: {str(e)}')
                )

    def update_profile(self, user):
        """Update the automatically created profile with generated data"""
        fake = Faker(['es_MX'])

        # Generate a random date of birth (18-60 years ago)
        today = timezone.now().date()
        age = random.randint(18, 60)
        date_of_birth = today - timedelta(days=age * 365 + random.randint(0, 365))

        # Generate profile data
        profile_data = {
            'user': user.id,
            'CURP': self.generate_curp(user, date_of_birth),
            'gender': random.choice(['M', 'F']),
            'date_of_birth': date_of_birth,
            'city': fake.city(),
            'zip_code': str(random.randint(10000, 99999))
        }

        try:
            # Get the existing profile
            profile = Profile.objects.get(user=user)

            # Use ProfileSerializer to update the profile
            serializer = ProfileSerializer(profile, data=profile_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return True
        except Profile.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Profile not found for user {user.username}')
            )
            return False
        except DRFValidationError as e:
            self.stdout.write(
                self.style.ERROR(f'Validation error updating profile for {user.username}: {str(e)}')
            )
            return False
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error updating profile for {user.username}: {str(e)}')
            )
            return False

    def generate_secure_password(self):
        """Generate a secure random password"""
        length = random.randint(10, 14)
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for i in range(length))
        # Ensure at least one of each required character type
        password = (password +
                    random.choice(string.ascii_uppercase) +
                    random.choice(string.ascii_lowercase) +
                    random.choice(string.digits) +
                    random.choice("!@#$%^&*"))
        return password

    def generate_curp(self, user, date_of_birth):
        """Generate a CURP-like ID (Mexican format)"""
        # First letter of first last name
        curp = user.last_name[0].upper()

        # First vowel of first last name
        vowels = ''.join(c for c in user.last_name[1:] if c.lower() in 'aeiou')
        curp += vowels[0].upper() if vowels else 'X'

        # First letter of second last name
        curp += (user.last_name2[0] if user.last_name2 else 'X').upper()

        # First letter of first name
        curp += user.first_name[0].upper()

        # Date of birth
        curp += date_of_birth.strftime('%y%m%d')

        # Gender
        gender = random.choice(['H', 'M'])  # H for male, M for female
        curp += gender

        # State code (example for Estado de México)
        curp += 'MC'

        # First internal consonant of first last name
        consonants = ''.join(c for c in user.last_name[1:] if c.lower() not in 'aeiou')
        curp += consonants[0].upper() if consonants else 'X'

        # First internal consonant of second last name
        consonants = ''.join(c for c in (user.last_name2 or 'X')[1:] if c.lower() not in 'aeiou')
        curp += consonants[0].upper() if consonants else 'X'

        # First internal consonant of first name
        consonants = ''.join(c for c in user.first_name[1:] if c.lower() not in 'aeiou')
        curp += consonants[0].upper() if consonants else 'X'

        # Add two random alphanumeric characters
        curp += random.choice(string.ascii_uppercase + string.digits)
        curp += random.choice(string.digits)

        return curp
