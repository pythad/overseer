# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DistributorGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(blank=True)),
                ('mentions', models.PositiveIntegerField(default=0, blank=True, verbose_name='number of mentions')),
                ('photo_url', models.URLField(null=True, blank=True, verbose_name='photo')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('vk_id', models.CharField(blank=True, max_length=15, verbose_name='vk id')),
                ('favorite', models.BooleanField(default=False, verbose_name='favorite')),
                ('is_closed', models.PositiveIntegerField(null=True, choices=[(0, 'open'), (1, 'closed'), (2, 'private')], blank=True, verbose_name='Whether the community is closed')),
                ('type', models.CharField(choices=[('group', 'group'), ('page', 'public page'), ('event', 'event')], max_length=5, blank=True)),
                ('members_count', models.PositiveIntegerField(null=True, blank=True)),
                ('contacts', models.TextField(blank=True)),
                ('user', models.ForeignKey(related_name='distributors_groups_of_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Distributor groups',
                'verbose_name': 'Distributor group',
            },
        ),
    ]
