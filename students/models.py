from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _

from .common import *
from django.db import models


class Student(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='students')
    student_name = models.CharField(_('Student name'), max_length=200, blank=False, null=False)
    height_feet = models.CharField(_('Height Feet'), max_length=10, blank=True, null=True)
    height_inch = models.CharField(_('Height Inch'), max_length=10, blank=True, null=True)
    weight = models.DecimalField(_('Weight'), max_digits=6, decimal_places=2, default=0.00)
    dob = models.DateField(_('Date of birth'), default=None, null=True, blank=True)
    grade = models.CharField(_('Grade'), max_length=100, blank=True, null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True)
    profile_image = models.ImageField(upload_to=file_upload, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.student_name

    @property
    def short_notes(self):
        return truncatechars(self.notes, 30)

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.profile_image
            self.profile_image = None
            super(self.__class__, self).save(*args, **kwargs)
            self.profile_image = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super(self.__class__, self).save(*args, **kwargs)


class Album(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='album')
    grade = models.CharField(_('Grade'), max_length=100, blank=True, null=True)
    height_feet = models.IntegerField(_('Height Feet'), blank=True, default=0)
    height_inch = models.IntegerField(_('Height Inch'), blank=True, default=0)
    weight = models.DecimalField(_('Weight'), max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to=file_upload, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.grade

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        ordering = ['-id']


class ReportCard(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='report_card')
    grade = models.CharField(_('Grade'), max_length=100, blank=True, null=True)
    doc_title = models.CharField(_('Document title'), max_length=100, blank=False, null=False)
    report_card = models.FileField(upload_to=file_upload, blank=True, null=True, validators=[file_validation])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doc_title

    class Meta:
        verbose_name = _('Report Card')
        verbose_name_plural = _('Report Cards')
        ordering = ['-id']


class SpecialServiceCategory(models.Model):
    category = models.CharField(_('Category'), max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = _('Special service category')
        verbose_name_plural = _('Special service categories')
        ordering = ['-id']
        

class SpecialService(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='special_service')
    category = models.ForeignKey('SpecialServiceCategory', on_delete=models.CASCADE, related_name='special_service')
    grade = models.CharField(_('Grade'), max_length=100, blank=True, null=True)
    doc_title = models.CharField(_('Document title'), max_length=100, blank=False, null=False)
    document = models.FileField(upload_to=file_upload, blank=True, null=True, validators=[file_validation])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doc_title

    class Meta:
        verbose_name = _('Special Service')
        verbose_name_plural = _('Special Services')
        ordering = ['-id']


class Immunization(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='immunization')
    doc_title = models.CharField(_('Document title'), max_length=100, blank=False, null=False)
    document = models.FileField(upload_to=file_upload, blank=True, null=True, validators=[file_validation])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doc_title

    class Meta:
        verbose_name = _('Immunization')
        verbose_name_plural = _('Immunizations')
        ordering = ['-id']


class OtherDocument(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='other_doc')
    doc_title = models.CharField(_('Document title'), max_length=100, blank=False, null=False)
    document = models.FileField(upload_to=file_upload, blank=True, null=True, validators=[file_validation])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doc_title

    class Meta:
        verbose_name = _('OtherDocument')
        verbose_name_plural = _('OtherDocuments')
        ordering = ['-id']