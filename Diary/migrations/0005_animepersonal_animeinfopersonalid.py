# Generated by Django 3.1 on 2020-08-25 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diary', '0004_animeinfopersonal'),
    ]

    operations = [
        migrations.AddField(
            model_name='animepersonal',
            name='animeInfoPersonalId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
