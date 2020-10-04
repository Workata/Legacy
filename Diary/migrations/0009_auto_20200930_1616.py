# Generated by Django 3.1.1 on 2020-09-30 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diary', '0008_auto_20200926_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='MangaInfoPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('writtenBy', models.CharField(max_length=250, null=True)),
                ('illustratedBy', models.CharField(max_length=250, null=True)),
                ('publishedBy', models.CharField(max_length=250, null=True)),
                ('englishPublisher', models.CharField(max_length=250, null=True)),
                ('imprint', models.CharField(max_length=250, null=True)),
                ('magazine', models.CharField(max_length=250, null=True)),
                ('demographic', models.CharField(max_length=250, null=True)),
                ('originalRun', models.CharField(max_length=250, null=True)),
                ('Volumes', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MangaPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('status', models.CharField(max_length=250)),
                ('finishedVolumes', models.IntegerField()),
                ('endDate', models.DateField()),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(null=True)),
                ('mangaInfoPersonalId', models.IntegerField(null=True)),
                ('mangaGlobalId', models.IntegerField(null=True)),
                ('userId', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='animepersonal',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
