from rest_framework import serializers
from .models import (
    ScholarshipCategory,
    RequiredDocument,
    Scholarship,
    Application,
    ApplicationDocument
)

class RequiredDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocument
        fields = ['id', 'category', 'file', 'description', 'name']

class RequiredDocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocument
        fields = ['id', 'name', 'description', 'file']

class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'profile', 'application_date', 'status']

# Serializer for creating/updating scholarships
class ScholarshipCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipCategory
        fields = ['id', 'name', 'description']

class ScholarshipCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = [
            'id',
            'category',
            'convocatoria',
            'description',
            'status',
            'application_start_date',
            'application_end_date'
        ]

    def validate(self, data):
        # Validate that end date is after start date
        if data.get('application_start_date') and data.get('application_end_date'):
            if data['application_end_date'] < data['application_start_date']:
                raise serializers.ValidationError(
                    "End date must be after start date"
                )
        return data

# Detailed serializer for retrieving scholarships
class ScholarshipDetailSerializer(serializers.ModelSerializer):
    category = ScholarshipCategoryDetailSerializer(read_only=True)
    required_documents = RequiredDocumentDetailSerializer(
        source='category.documents',
        many=True,
        read_only=True
    )
    applications_count = serializers.SerializerMethodField()
    recent_applications = ApplicationListSerializer(
        source='applications',
        many=True,
        read_only=True
    )

    class Meta:
        model = Scholarship
        fields = [
            'id',
            'category',
            'convocatoria',
            'description',
            'status',
            'application_start_date',
            'application_end_date',
            'required_documents',
            'applications_count',
            'recent_applications'
        ]

    def get_applications_count(self, obj):
        return obj.applications.count()

# List serializer for scholarship overview
class ScholarshipListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Scholarship
        fields = [
            'id',
            'category_name',
            'description',
            'status',
            'application_start_date',
            'application_end_date',
            'applications_count'
        ]

    def get_applications_count(self, obj):
        return obj.applications.count()

class ScholarshipCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipCategory
        fields = ['id', 'name', 'description']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'profile', 'scholarship', 'application_date', 'status']
        read_only_fields = ['application_date']

class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = ['id', 'application', 'document_id', 'upload_date', 'status']
        read_only_fields = ['upload_date']
