from django.contrib import admin
from jmespath import search

from .models import *


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'grade', 'dob', 'short_notes']
    search_fields = ['student_name']
    list_per_page = 25


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['student', 'grade', 'image']
    search_fields = ['grade']
    list_per_page = 25


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['grade', 'doc_title']
    search_fields = ['doc_title']
    list_per_page = 25


@admin.register(SpecialServiceCategory)
class SpecialServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'is_active']
    search_fields = ['category']
    list_per_page = 25


@admin.register(SpecialService)
class SpecialServiceAdmin(admin.ModelAdmin):
    list_display = ['category', 'doc_title']
    search_fields = ['doc_title']
    list_per_page = 25


@admin.register(Immunization)
class ImmunizationAdmin(admin.ModelAdmin):
    list_display = ['doc_title']
    search_fields = ['doc_title']
    list_per_page = 25


@admin.register(OtherDocument)
class OtherDocumentAdmin(admin.ModelAdmin):
    list_display = ['doc_title']
    search_fields = ['doc_title']
    list_per_page = 25
