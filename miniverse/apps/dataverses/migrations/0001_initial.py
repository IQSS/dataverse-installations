# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dvobjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataverse',
            fields=[
                ('id', models.OneToOneField(primary_key=True, db_column=b'id', serialize=False, to='dvobjects.DvObject')),
                ('affiliation', models.CharField(max_length=255, null=True, blank=True)),
                ('alias', models.CharField(max_length=255)),
                ('dataversetype', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('displaybytype', models.NullBooleanField()),
                ('facetroot', models.BooleanField()),
                ('guestbookroot', models.BooleanField()),
                ('metadatablockroot', models.BooleanField()),
                ('name', models.CharField(max_length=255)),
                ('permissionroot', models.BooleanField(default=True)),
                ('templateroot', models.BooleanField()),
                ('themeroot', models.BooleanField()),
            ],
            options={
                'db_table': 'dataverse',
                'managed': False,
            },
        ),
    ]
