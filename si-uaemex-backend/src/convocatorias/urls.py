from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ScholarshipCategoryViewSet,
    RequiredDocumentViewSet,
    ScholarshipViewSet,
    ApplicationViewSet,
    ApplicationDocumentViewSet
)

convocatorias_router = DefaultRouter()
convocatorias_router.register(r'categories', ScholarshipCategoryViewSet)
convocatorias_router.register(r'required-documents', RequiredDocumentViewSet)
convocatorias_router.register(r'scholarships', ScholarshipViewSet, basename='scholarship')
convocatorias_router.register(r'applications', ApplicationViewSet, basename='application')
convocatorias_router.register(r'application-documents', ApplicationDocumentViewSet, basename='application-document')
urlpatterns = [
    path('', include(convocatorias_router.urls)),
]
