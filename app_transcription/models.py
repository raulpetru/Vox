import os
import secrets

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


# name=secrets.token_urlsafe(16)

def file_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    randomstr = secrets.token_urlsafe(16)
    return 'recordings/{basename}_{randomstring}{ext}'.format(userid=instance.user.id,
                                                             basename=basefilename,
                                                             randomstring=randomstr, ext=file_extension)


class Recording(models.Model):
    name = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to=file_path, validators=[FileExtensionValidator(
        ['opus', 'flac', 'webm', 'weba', 'wav', 'ogg', 'm4a', 'oga', 'mid', 'mp3', 'aiff', 'wma', 'au'])])
    upload_date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [('Pending', 'Pending'), ('Processed', 'Processed')]
    transcription_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    transcription_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-upload_date_time']


def generate_api():
    return secrets.token_urlsafe(16)


class APIClient(models.Model):
    client_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=50, default=generate_api)

    def __str__(self):
        return f'{self.client_name}: {self.api_key}'
