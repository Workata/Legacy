# Generated by Django 3.1 on 2020-08-22 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnimeGlobal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('directedBy', models.CharField(max_length=150)),
                ('producedBy', models.CharField(max_length=150)),
                ('writtenBy', models.CharField(max_length=150)),
                ('musicBy', models.CharField(max_length=150)),
                ('studio', models.CharField(max_length=150)),
                ('licensedBy', models.CharField(max_length=150)),
                ('originalNetwork', models.CharField(max_length=150)),
                ('originalRun', models.CharField(max_length=150)),
                ('episodes', models.IntegerField()),
            ],
        ),
    ]
