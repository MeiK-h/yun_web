from django import forms
from django.core.exceptions import ValidationError

from .models import UploadFile


def file_valid(value):
    file_size = value.size
    if file_size > 256 * 1024 * 1024:  # 256 MB
        raise ValidationError("文件过大")


class UploadFileForm(forms.Form):
    upload = forms.FileField(validators=[file_valid])
    file_type = forms.ChoiceField(choices=UploadFile.file_type_choices)
