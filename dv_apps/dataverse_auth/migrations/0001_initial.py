# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tokenstring', models.CharField(unique=True, max_length=255)),
                ('disabled', models.BooleanField()),
                ('expiretime', models.DateTimeField()),
                ('createtime', models.DateTimeField()),
            ],
            options={
                'ordering': ('-expiretime', 'authenticateduser'),
                'db_table': 'apitoken',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthenticatedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('useridentifier', models.CharField(unique=True, max_length=255)),
                ('affiliation', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('firstname', models.CharField(max_length=255, null=True, blank=True)),
                ('lastname', models.CharField(max_length=255, null=True, blank=True)),
                ('modificationtime', models.DateTimeField(null=True, blank=True)),
                ('position', models.CharField(max_length=255, null=True, blank=True)),
                ('superuser', models.NullBooleanField()),
            ],
            options={
                'ordering': ('useridentifier',),
                'db_table': 'authenticateduser',
                'managed': False,
            },
        ),
    ]
