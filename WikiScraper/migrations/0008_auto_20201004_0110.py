# Generated by Django 3.1.1 on 2020-10-03 23:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WikiScraper', '0007_animeglobal_englishnetwok'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animeglobal',
            old_name='englishNetwok',
            new_name='englishNetwork',
        ),
    ]
