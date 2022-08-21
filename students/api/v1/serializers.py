from dataclasses import field
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from students.models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['user', 'is_active']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        exclude = ['is_active']


class ReportCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCard
        exclude = ['is_active']


class SpecialServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialServiceCategory
        exclude = ['is_active']


class SpecialServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialService
        exclude = ['is_active']


class ImmunizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Immunization
        exclude = ['is_active']


class OtherDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherDocument
        exclude = ['is_active']
