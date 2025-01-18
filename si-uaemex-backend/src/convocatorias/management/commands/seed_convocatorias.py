from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
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
from faker import Faker
import requests
from io import BytesIO
from PIL import Image
import os
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with convocatorias data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write('Flushing existing data...')
            ApplicationDocument.objects.all().delete()
            Application.objects.all().delete()
            Scholarship.objects.all().delete()
            RequiredDocument.objects.all().delete()
            ScholarshipCategory.objects.all().delete()
            File.objects.all().delete()

        self.stdout.write('Starting convocatorias seeding...')

        # Get or create admin user for file authorship
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpass123'
            )

        self.admin_user = admin_user
        self.fake = Faker(['es_MX'])

        # Create sample files first
        self.sample_files = self.create_sample_files()

        # Create other data
        self.seed_scholarship_categories()
        self.seed_required_documents()
        self.seed_scholarships()
        self.seed_applications()

        self.stdout.write(self.style.SUCCESS('Successfully seeded convocatorias data'))

    def create_sample_files(self):
        """Create sample files of different types"""
        self.stdout.write('Creating sample files...')

        files = []

        # Create PDF files
        for i in range(3):
            pdf_content = SimpleUploadedFile(
                name=f'sample_doc_{i}.pdf',
                content=b'%PDF-1.4 Sample PDF content',
                content_type='application/pdf'
            )
            file = File.objects.create(
                file=pdf_content,
                author=self.admin_user
            )
            files.append(file)

        # Create image files
        for i in range(3):
            # Create a simple image
            image = Image.new('RGB', (800, 600), color='white')
            image_io = BytesIO()
            image.save(image_io, format='JPEG')

            image_file = SimpleUploadedFile(
                name=f'sample_image_{i}.jpg',
                content=image_io.getvalue(),
                content_type='image/jpeg'
            )

            file = File.objects.create(
                file=image_file,
                author=self.admin_user
            )
            files.append(file)

        # Create document files
        for i in range(3):
            doc_content = SimpleUploadedFile(
                name=f'sample_doc_{i}.docx',
                content=b'Sample document content',
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            file = File.objects.create(
                file=doc_content,
                author=self.admin_user
            )
            files.append(file)

        return files

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

        created_categories = []
        for category_data in categories:
            category, created = ScholarshipCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            created_categories.append(category)

        return created_categories

    def seed_required_documents(self):
        self.stdout.write('Seeding required documents...')

        documents = [
            'Official Transcript',
            'Identification Document',
            'Proof of Income',
            'Recommendation Letter',
            'Study Plan',
            'Language Certificate',
            'Medical Certificate'
        ]

        for category in ScholarshipCategory.objects.all():
            # Select 3-5 random documents for each category
            num_docs = random.randint(3, 5)
            selected_docs = random.sample(documents, num_docs)

            for doc_name in selected_docs:
                RequiredDocument.objects.get_or_create(
                    name=f'{doc_name} - {category.name}',
                    defaults={
                        'category': category,
                        'file': random.choice(self.sample_files),
                        'description': f'Please provide your {doc_name.lower()} according to the specified format.'
                    }
                )

    def seed_scholarships(self):
        self.stdout.write('Seeding scholarships...')

        current_date = timezone.now().date()

        for category in ScholarshipCategory.objects.all():
            # Past scholarship
            start_date = current_date - timedelta(days=random.randint(60, 90))
            end_date = current_date - timedelta(days=random.randint(10, 30))

            Scholarship.objects.create(
                category=category,
                convocatoria=random.choice(self.sample_files),
                description=self.fake.paragraph(),
                status=ScholarshipStatus.CLOSED,
                application_start_date=start_date,
                application_end_date=end_date
            )

            # Current scholarship
            start_date = current_date - timedelta(days=random.randint(5, 15))
            end_date = current_date + timedelta(days=random.randint(15, 30))

            Scholarship.objects.create(
                category=category,
                convocatoria=random.choice(self.sample_files),
                description=self.fake.paragraph(),
                status=ScholarshipStatus.ACCEPTING_APPLICATIONS,
                application_start_date=start_date,
                application_end_date=end_date
            )

            # Future scholarship
            start_date = current_date + timedelta(days=random.randint(15, 30))
            end_date = current_date + timedelta(days=random.randint(45, 60))

            Scholarship.objects.create(
                category=category,
                convocatoria=random.choice(self.sample_files),
                description=self.fake.paragraph(),
                status=ScholarshipStatus.CLOSED,
                application_start_date=start_date,
                application_end_date=end_date
            )

    def seed_applications(self):
        self.stdout.write('Seeding applications...')

        active_scholarships = Scholarship.objects.filter(
            status=ScholarshipStatus.ACCEPTING_APPLICATIONS
        )
        profiles = Profile.objects.all()

        if not profiles.exists():
            self.stdout.write(self.style.WARNING('No profiles found. Skipping applications seeding.'))
            return

        for scholarship in active_scholarships:
            # Create 3-7 applications per scholarship
            num_applications = random.randint(3, 7)
            selected_profiles = random.sample(list(profiles), min(num_applications, profiles.count()))

            for profile in selected_profiles:
                application = Application.objects.create(
                    profile=profile,
                    scholarship=scholarship,
                    status=random.choice(list(ApplicationStatus.values))
                )

                # Create application documents
                self.create_application_documents(application)

    def create_application_documents(self, application):
        required_docs = RequiredDocument.objects.filter(
            category=application.scholarship.category
        )

        for required_doc in required_docs:
            ApplicationDocument.objects.create(
                application=application,
                document_id=random.choice(self.sample_files),
                status=random.choice(list(ApplicationStatus.values))
            )
