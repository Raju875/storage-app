import os.path
from django.utils import timezone
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import ImageFieldFile, FieldFile


def file_validation(value):
    """
    Common image/attachment validation check
    """
    if value and isinstance(value, UploadedFile):
        MIME_TYPE = ['jpg', 'jpeg', 'png', 'pdf', 'doc']
        MAX_UPLOAD_SIZE = 2
        file_type = value.content_type.split('/')[-1]
        if file_type not in MIME_TYPE:
            raise serializers.ValidationError(
                _('{file_type} file not supported. Please upload image, pdf or doc file'.format(
                    file_type=file_type.upper())
                    )
                )
        file_size = value.size/(1024*1024)
        if file_size > 2:
            raise serializers.ValidationError(
                _('Please keep filesize under {MAX_UPLOAD_SIZE}MB. Current filesize {file_size}MB').format(
                    MAX_UPLOAD_SIZE=MAX_UPLOAD_SIZE, file_size=round(file_size, 3)
                    )
                )
    else:
        pass


def file_upload(instance, filename, *args, **kwargs):
    """
    Common image/attachment upload
    """
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    new_filename = f"{now:%d%H%M%S}-{now.microsecond}{extension}"

    if instance.__class__.__name__ == 'Student':
        dir_id = instance.id
        directory = 'profile'
    else:
        dir_id = instance.student.id
        directory = instance.__class__.__name__.lower()

    file_path = f"uploads/student_{dir_id}/{directory}"
    return os.path.join(file_path, new_filename)
