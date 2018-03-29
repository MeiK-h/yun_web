from django.db import models
from django.contrib.auth import get_user_model


class UploadFile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # 所属用户
    upload = models.FileField(upload_to='%Y/%m/')

    file_type_choices = (
        ('private', '私有文件'),
        ('public', '公共文件')
    )
    file_type = models.CharField(max_length=15, choices=file_type_choices, default=file_type_choices[0][0])  # 文件类型

    upload_time = models.DateTimeField(auto_now=True)  # 上传时间
