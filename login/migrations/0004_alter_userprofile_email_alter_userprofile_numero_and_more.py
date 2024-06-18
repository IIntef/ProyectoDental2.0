# Generated by Django 5.0.6 on 2024-06-18 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_remove_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='numero',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tipo',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
