# Generated by Django 3.1.1 on 2020-09-30 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Diary', '0009_auto_20200930_1616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mangainfopersonal',
            old_name='Volumes',
            new_name='volumes',
        ),
    ]