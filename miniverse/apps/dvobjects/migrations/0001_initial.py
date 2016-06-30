# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DvObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dtype', models.CharField(max_length=31, choices=[(b'Dataverse', b'Dataverse'), (b'Dataset', b'Dataset'), (b'DataFile', b'DataFile')])),
                ('createdate', models.DateTimeField(auto_now_add=True)),
                ('modificationtime', models.DateTimeField(auto_now=True)),
                ('indextime', models.DateTimeField(null=True, blank=True)),
                ('permissionindextime', models.DateTimeField(null=True, blank=True)),
                ('permissionmodificationtime', models.DateTimeField(null=True, blank=True)),
                ('publicationdate', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dvobject',
                'managed': False,
            },
        ),
    ]
