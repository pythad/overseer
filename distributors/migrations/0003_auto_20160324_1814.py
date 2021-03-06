# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-24 18:14
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0002_auto_20160104_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username'),
        ),
    ]
