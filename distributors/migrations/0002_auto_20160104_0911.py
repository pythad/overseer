# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('distributors', '0001_initial'),
        ('groups', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='distributors_groups',
            field=models.ManyToManyField(related_name='distributors_groups_of_queries', to='groups.DistributorGroup', blank=True),
        ),
        migrations.AddField(
            model_name='query',
            name='distributors_persons',
            field=models.ManyToManyField(related_name='distributors_persons_of_queries', to='people.DistributorPerson', blank=True),
        ),
        migrations.AddField(
            model_name='query',
            name='section',
            field=models.ForeignKey(related_name='section_queries', blank=True, null=True, to='distributors.Section'),
        ),
        migrations.AddField(
            model_name='query',
            name='user',
            field=models.ForeignKey(related_name='user_queries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(related_name='user_set', blank=True, verbose_name='groups', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(related_name='user_set', blank=True, verbose_name='user permissions', related_query_name='user', help_text='Specific permissions for this user.', to='auth.Permission'),
        ),
    ]
