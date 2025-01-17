from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    ScholarshipCategory,
    RequiredDocument,
    Scholarship,
    Application,
    ApplicationDocument,
    ScholarshipStatus,
    ApplicationStatus
)
from .serializers import (
    RequiredDocumentSerializer,
    ApplicationSerializer,
    ApplicationDocumentSerializer,
    ScholarshipCreateUpdateSerializer,
    ScholarshipDetailSerializer,
    ScholarshipListSerializer,
    ScholarshipCategorySerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class ScholarshipCategoryViewSet(viewsets.ModelViewSet):
    queryset = ScholarshipCategory.objects.all()
    serializer_class = ScholarshipCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class RequiredDocumentViewSet(viewsets.ModelViewSet):
    queryset = RequiredDocument.objects.all()
    serializer_class = RequiredDocumentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = RequiredDocument.objects.all()
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'application_start_date', 'application_end_date']
    search_fields = ['description', 'category__name']
    ordering_fields = ['application_start_date', 'application_end_date']
    ordering = ['-application_start_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return ScholarshipListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ScholarshipCreateUpdateSerializer
        return ScholarshipDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'change_status']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = Scholarship.objects.all()

        # Filter by active status
        active = self.request.query_params.get('active', None)
        if active is not None:
            today = timezone.now().date()
            if active.lower() == 'true':
                queryset = queryset.filter(
                    application_start_date__lte=today,
                    application_end_date__gte=today,
                    status=ScholarshipStatus.ACCEPTING_APPLICATIONS
                )

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(
                application_start_date__gte=start_date,
                application_end_date__lte=end_date
            )

        return queryset

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        scholarship = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ScholarshipStatus.values:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        scholarship.status = new_status
        scholarship.save()
        serializer = self.get_serializer(scholarship)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def applications_summary(self, request, pk=None):
        scholarship = self.get_object()
        applications = scholarship.applications.all()

        summary = {
            'total_applications': applications.count(),
            'status_breakdown': {},
            'daily_applications': {}
        }

        # Count applications by status
        for status_choice in ApplicationStatus.choices:
            count = applications.filter(status=status_choice[0]).count()
            summary['status_breakdown'][status_choice[1]] = count

        # Get daily application counts
        from django.db.models import Count
        from django.db.models.functions import TruncDate

        daily_counts = applications.annotate(
            date=TruncDate('application_date')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        for entry in daily_counts:
            summary['daily_applications'][str(entry['date'])] = entry['count']

        return Response(summary)


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(profile__user=user)

    def perform_create(self, serializer):
        scholarship = serializer.validated_data['scholarship']

        # Check if scholarship is accepting applications
        if scholarship.status != ScholarshipStatus.ACCEPTING_APPLICATIONS:
            raise serializers.ValidationError(
                "This scholarship is not accepting applications"
            )

        # Check if application period is valid
        today = timezone.now().date()
        if not (scholarship.application_start_date <= today <= scholarship.application_end_date):
            raise serializers.ValidationError(
                "Application period is not active"
            )

        serializer.save()

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')

        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff members can change application status'},
                status=status.HTTP_403_FORBIDDEN
            )

        if new_status not in ApplicationStatus.values:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()

        return Response(ApplicationSerializer(application).data)


class ApplicationDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ApplicationDocument.objects.all()
        return ApplicationDocument.objects.filter(application__profile__user=user)

    def perform_create(self, serializer):
        application = serializer.validated_data['application']

        # Ensure user can only upload documents to their own applications
        if not self.request.user.is_staff and application.profile.user != self.request.user:
            raise serializers.ValidationError(
                "You can only upload documents to your own applications"
            )

        serializer.save()
