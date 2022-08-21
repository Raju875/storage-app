from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter

from students.models import *
from .serializers import *


class StudentViewSet(ModelViewSet):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    serializer_class = StudentSerializer
    filter_backends = [SearchFilter]
    queryset = Student.objects.none()

    search_fields = ['student_name', 'height_feet', 'height_inch', 'weight', 'dob', 'grade']

    def get_queryset(self):
        return Student.objects.select_related('user').filter(user=self.request.user)

    def perform_create(self, serializer):
        student = serializer.save(user=self.request.user)
        Album.objects.create(student=student,
                             grade=student.grade,
                             height_feet=student.height_feet,
                             height_inch=student.height_inch,
                             weight=student.weight,
                             image=student.profile_image)

    def perform_update(self, serializer):
        student = serializer.save(user=self.request.user)
        Album.objects.filter(student=student).update(
                             grade=student.grade,
                             height_feet=student.height_feet,
                             height_inch=student.height_inch,
                             weight=student.weight,
                             image=student.profile_image)


class AlbumViewSet(ModelViewSet):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    serializer_class = AlbumSerializer
    queryset = Album.objects.none()

    def get_queryset(self):
        return Album.objects.filter(student__user=self.request.user).filter(is_active=True)


class GetAlbum(APIView):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]

    def get(self, request, student_id):
        data = Album.objects.filter(student_id=student_id).filter(student__user=self.request.user).filter(is_active=True)
        return Response(AlbumSerializer(data, many=True).data, status=status.HTTP_200_OK)


class ReportCardViewSet(ModelViewSet):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    serializer_class = ReportCardSerializer
    queryset = ReportCard.objects.none()

    def get_queryset(self):
        return ReportCard.objects.filter(student__user=self.request.user).filter(is_active=True)


class GetReportCard(APIView):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]

    def get(self, request, student_id):
        data = ReportCard.objects.filter(student_id=student_id).filter(
            student__user=self.request.user).filter(is_active=True)
        return Response(ReportCardSerializer(data, many=True).data, status=status.HTTP_200_OK)


class SpecialServiceCategoryViewSet(ModelViewSet):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    http_method_names = ['get']
    serializer_class = SpecialServiceCategorySerializer
    queryset = SpecialServiceCategory.objects.filter(is_active=True)


class SpecialServiceViewSet(ModelViewSet):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    serializer_class = SpecialServiceSerializer
    queryset = SpecialService.objects.none()

    def get_queryset(self):
        return SpecialService.objects.filter(student__user__id=self.request.user.id).filter(is_active=True)


class GetSpecialService(APIView):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]

    def get(self, request, category_id, student_id):
        data = SpecialService.objects.filter(category_id=category_id,student_id=student_id,student__user=self.request.user,is_active=True)
        return Response(SpecialServiceSerializer(data, many=True).data, status=status.HTTP_200_OK)


class ImmunizationViewSet(ModelViewSet):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    serializer_class = ImmunizationSerializer
    queryset = Immunization.objects.none()

    def get_queryset(self):
        return Immunization.objects.filter(student__user__id=self.request.user.id).filter(is_active=True)

class GetImmunization(APIView):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]

    def get(self, request, student_id):
        data = Immunization.objects.filter(student_id=student_id).filter(student__user=self.request.user).filter(is_active=True)
        return Response(ImmunizationSerializer(data, many=True).data, status=status.HTTP_200_OK)


class OtherDocumentViewSet(ModelViewSet):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]
    serializer_class = OtherDocumentSerializer
    queryset = OtherDocument.objects.none()

    def get_queryset(self):
        return OtherDocument.objects.filter(student__user__id=self.request.user.id).filter(is_active=True)


class GetOtherDocument(APIView):
    authentication_class = [TokenAuthentication, SessionAuthentication]
    permission_class = [IsAuthenticated]

    def get(self, request, student_id):
        data = OtherDocument.objects.filter(student_id=student_id).filter(student__user=self.request.user).filter(is_active=True)
        return Response(OtherDocumentSerializer(data, many=True).data, status=status.HTTP_200_OK)


# All students related list & details
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def GetData(request, pk=None):
    students = []
    report_cards = []
    special_services = []
    immunizations = []
    other_docs = []

    data_infos = Student.objects.filter(user=request.user.id).filter(is_active=True).prefetch_related(
        'report_card', 'special_service', 'immunization', 'other_doc'
        )

    if pk is not None:
        data_infos = data_infos.filter(pk=pk)

    if data_infos:
        students = StudentSerializer(data_infos, many=True).data
        for info in data_infos:
            report_cards.append(ReportCardSerializer(info.report_card.all(), many=True).data)
            special_services.append(SpecialServiceSerializer(info.special_service.all(), many=True).data)
            immunizations.append(ImmunizationSerializer(info.immunization.all(), many=True).data)
            other_docs.append(OtherDocumentSerializer(info.other_doc.all(), many=True).data)

    context = {
        'students': students,
        'report_cards': report_cards,
        'special_services':special_services,
        'immunizations': immunizations,
        'other_docs': other_docs
        }     
    return Response(context)