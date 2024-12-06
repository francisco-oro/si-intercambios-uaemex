from django.db import models
from django.contrib.auth import get_user_model
from src.files.models import File
from src.users.models import Profile

User = get_user_model()

# Enum choices for Scholarship Status
class ScholarshipStatus(models.TextChoices):
    ACCEPTING_APPLICATIONS = 'accepting', 'Accepting Applications'
    CLOSED = 'closed', 'Closed'
    SUSPENDED = 'suspended', 'Suspended'
    APPLICATIONS_PENDING = 'pending', 'Applications pending'

# Enum choices for Application Status
class ApplicationStatus(models.TextChoices):
    OPEN = 'open', 'Open'
    CLOSED = 'closed', 'Closed'
    AWAITING_RESPONSE = 'awaiting_response', 'Awaiting Response'
    CANCELLED = 'cancelled', 'Cancelled'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'
    USER_REVIEW_REQUIRED = 'user review required', 'User review required'

class ApplicationDocumentStatus(models.TextChoices):
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'
    AWAITING_RESPONSE = 'awaiting_response', 'Awaiting Response'

class ScholarshipCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=320, unique=True)

    def __str__(self):
        return self.name


class RequiredDocument(models.Model):
    category = models.ForeignKey(ScholarshipCategory, on_delete=models.CASCADE, related_name='documents')
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='documents')
    description = models.TextField()
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.description


class Scholarship(models.Model):
    category = models.ForeignKey(ScholarshipCategory, on_delete=models.CASCADE, related_name='scholarships')
    convocatoria = models.ForeignKey(File, on_delete=models.CASCADE, related_name='scholarships')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=ScholarshipStatus.choices, default=ScholarshipStatus.CLOSED)
    application_start_date = models.DateField()
    application_end_date = models.DateField()

    def __str__(self):
        return f"Scholarship {self.id} - {self.category.name}"


class Application(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='applications')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.OPEN)

    def __str__(self):
        return f"Application {self.id} by {self.user.profile.CURP}"


class ApplicationDocument(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='application_documents')
    document_id = models.ForeignKey(File, on_delete=models.CASCADE, related_name='application_documents')
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.OPEN)

    def __str__(self):
        return f"Document {self.id} for Application {self.application.id}"
