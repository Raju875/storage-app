from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets
router = DefaultRouter()

router.register('basic-info', viewsets.StudentViewSet, basename='students')
router.register('album', viewsets.AlbumViewSet, basename='album')
router.register('report-card', viewsets.ReportCardViewSet, basename='report-card')
router.register('special-service-category', viewsets.SpecialServiceCategoryViewSet, basename='special-service-category')
router.register('special-service', viewsets.SpecialServiceViewSet, basename='special-service')
router.register('immunization', viewsets.ImmunizationViewSet, basename='immunization')
router.register('other-document', viewsets.OtherDocumentViewSet, basename='other-document')

urlpatterns = [
    path('get-album/<int:student_id>/', viewsets.GetAlbum.as_view()),
    path('get-report-card/<int:student_id>/', viewsets.GetReportCard.as_view()),
    path('get-special-service/<int:category_id>/<int:student_id>/', viewsets.GetSpecialService.as_view()),
    path('get-immunization/<int:student_id>/',viewsets.GetImmunization.as_view()),
    path('get-other-document/<int:student_id>/',viewsets.GetOtherDocument.as_view()),

    path('', include(router.urls)),
    path('get-data/', viewsets.GetData),
    path('get-data/<int:pk>/', viewsets.GetData),
]
