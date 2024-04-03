# Generated by Django 5.0.3 on 2024-04-03 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0005_song_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='duration',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='audio',
            name='waveform',
            field=models.JSONField(default=None),
        ),
    ]
