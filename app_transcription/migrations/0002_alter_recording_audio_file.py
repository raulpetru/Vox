# Generated by Django 5.0.3 on 2024-03-30 14:24

import app_transcription.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_transcription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='audio_file',
            field=models.FileField(upload_to=app_transcription.models.file_path, validators=[django.core.validators.FileExtensionValidator(['opus', 'flac', 'webm', 'weba', 'wav', 'ogg', 'm4a', 'oga', 'mid', 'mp3', 'aiff', 'wma', 'au', 'aac'])]),
        ),
    ]
