# Generated by Django 5.0.3 on 2024-04-25 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0021_alter_song_options_alter_userlibrary_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlibrary',
            name='songs',
            field=models.ManyToManyField(blank=True, to='core_api.song'),
        ),
    ]