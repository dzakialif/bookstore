# Generated by Django 5.1.4 on 2024-12-13 19:48

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_profile_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name=django.contrib.auth.models.User),
        ),
    ]
