# Generated by Django 5.0.3 on 2024-04-10 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0017_remove_audio_song'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserFavorite',
        ),
    ]
