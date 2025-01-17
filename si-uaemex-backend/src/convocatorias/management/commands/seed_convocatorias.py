from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from src.convocatorias.models import (
    ScholarshipCategory,
    RequiredDocument,
    Scholarship,
    Application,
    ApplicationDocument,
    ScholarshipStatus,
    ApplicationStatus
)
from src.files.models import File
from src.users.models import Profile
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with convocatorias data'

    def handle(self, *args, **options):
        self.stdout.write('Starting convocatorias seeding...')

        self.seed_scholarship_categories()
        self.seed_files()
        self.seed_required_documents()
        self.seed_scholarships()
        self.seed_applications()

        self.stdout.write(self.style.SUCCESS('Successfully seeded convocatorias data'))

    def seed_scholarship_categories(self):
        self.stdout.write('Seeding scholarship categories...')

        categories = [
            {
                'name': 'International Exchange',
                'description': 'Scholarships for international student exchange programs'
            },
            {
                'name': 'Research Grant',
                'description': 'Funding for research projects and academic investigations'
            },
            {
                'name': 'Merit-based Scholarship',
                'description': 'Scholarships awarded based on academic excellence'
            },
            {
                'name': 'Need-based Aid',
                'description': 'Financial assistance based on economic necessity'
            },
            {
                'name': 'Sports Scholarship',
                'description': 'Scholarships for outstanding athletic achievement'
            }
        ]

        for category_data in categories:
            ScholarshipCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )

    def seed_files(self):
        self.stdout.write('Seeding files...')

        file_types = ['pdf', 'doc', 'docx']
        for i in range(1, 6):
            file_type = random.choice(file_types)
            File.objects.get_or_create(
                name=f'Document_{i}',
                defaults={
                    'file': f'path/to/sample/file_{i}.{file_type}',
                    'content_type': f'application/{file_type}',
                    'size': random.randint(1000, 5000000)
                }
            )

    def seed_required_documents(self):
        self.stdout.write('Seeding required documents...')

        documents = [
            'Passport Copy',
            'Academic Transcript',
            'Recommendation Letter',
            'Motivation Letter',
            'Language Certificate',
            'CV/Resume',
            'Financial Statement'
        ]

        categories = ScholarshipCategory.objects.all()
        files = File.objects.all()

        for category in categories:
            # Select 3-5 random documents for each category
            num_docs = random.randint(3, 5)
            selected_docs = random.sample(documents, num_docs)

            for doc_name in selected_docs:
                RequiredDocument.objects.get_or_create(
                    name=f'{doc_name} - {category.name}',
                    defaults={
                        'category': category,
                        'file': random.choice(files),
                        'description': f'Please provide your {doc_name.lower()} according to the specified format.'
                    }
                )

    def seed_scholarships(self):
        self.stdout.write('Seeding scholarships...')

        categories = ScholarshipCategory.objects.all()
        files = File.objects.all()

        # Generate scholarships with different date ranges and statuses
        current_date = timezone.now().date()

        for category in categories:
            # Past scholarship
            start_date = current_date - timedelta(days=random.randint(60, 90))
            end_date = current_date - timedelta(days=random.randint(10, 30))
            Scholarship.objects.get_or_create(
                category=category,
                application_start_date=start_date,
                defaults={
                    'convocatoria': random.choice(files),
                    'description': f'Past scholarship for {category.name}',
                    'status': ScholarshipStatus.CLOSED,
                    'application_end_date': end_date
                }
            )

            # Current scholarship
            start_date = current_date - timedelta(days=random.randint(5, 15))
            end_date = current_date + timedelta(days=random.randint(15, 30))
            Scholarship.objects.get_or_create(
                category=category,
                application_start_date=start_date,
                defaults={
                    'convocatoria': random.choice(files),
                    'description': f'Current active scholarship for {category.name}',
                    'status': ScholarshipStatus.ACCEPTING_APPLICATIONS,
                    'application_end_date': end_date
                }
            )

            # Future scholarship
            start_date = current_date + timedelta(days=random.randint(15, 30))
            end_date = current_date + timedelta(days=random.randint(45, 60))
            Scholarship.objects.get_or_create(
                category=category,
                application_start_date=start_date,
                defaults={
                    'convocatoria': random.choice(files),
                    'description': f'Upcoming scholarship for {category.name}',
                    'status': ScholarshipStatus.CLOSED,
                    'application_end_date': end_date
                }
            )

    def seed_applications(self):
        self.stdout.write('Seeding applications...')

        # Get all active scholarships and profiles
        scholarships = Scholarship.objects.filter(
            status=ScholarshipStatus.ACCEPTING_APPLICATIONS
        )
        profiles = Profile.objects.all()

        if not profiles.exists():
            self.stdout.write(self.style.WARNING('No profiles found. Skipping applications seeding.'))
            return

        for scholarship in scholarships:
            # Create 3-7 applications per scholarship
            num_applications = random.randint(3, 7)
            selected_profiles = random.sample(list(profiles), min(num_applications, profiles.count()))

            for profile in selected_profiles:
                application, created = Application.objects.get_or_create(
                    profile=profile,
                    scholarship=scholarship,
                    defaults={
                        'status': random.choice(list(ApplicationStatus.values))
                    }
                )

                if created:
                    self.seed_application_documents(application)

    def seed_application_documents(self, application):
        files = File.objects.all()
        required_docs = RequiredDocument.objects.filter(
            category=application.scholarship.category
        )

        for required_doc in required_docs:
            ApplicationDocument.objects.create(
                application=application,
                document_id=random.choice(files),
                status=random.choice(list(ApplicationStatus.values))
            )
