# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datasetversion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unf', models.CharField(max_length=255, null=True, blank=True)),
                ('archivenote', models.CharField(max_length=1000, null=True, blank=True)),
                ('archivetime', models.DateTimeField(null=True, blank=True)),
                ('availabilitystatus', models.TextField(null=True, blank=True)),
                ('citationrequirements', models.TextField(null=True, blank=True)),
                ('conditions', models.TextField(null=True, blank=True)),
                ('confidentialitydeclaration', models.TextField(null=True, blank=True)),
                ('contactforaccess', models.TextField(null=True, blank=True)),
                ('createtime', models.DateTimeField()),
                ('dataaccessplace', models.TextField(null=True, blank=True)),
                ('deaccessionlink', models.CharField(max_length=255, null=True, blank=True)),
                ('depositorrequirements', models.TextField(null=True, blank=True)),
                ('disclaimer', models.TextField(null=True, blank=True)),
                ('fileaccessrequest', models.NullBooleanField()),
                ('inreview', models.NullBooleanField()),
                ('lastupdatetime', models.DateTimeField()),
                ('license', models.CharField(max_length=255, null=True, blank=True)),
                ('originalarchive', models.TextField(null=True, blank=True)),
                ('releasetime', models.DateTimeField(null=True, blank=True)),
                ('restrictions', models.TextField(null=True, blank=True)),
                ('sizeofcollection', models.TextField(null=True, blank=True)),
                ('specialpermissions', models.TextField(null=True, blank=True)),
                ('studycompletion', models.TextField(null=True, blank=True)),
                ('termsofaccess', models.TextField(null=True, blank=True)),
                ('termsofuse', models.TextField(null=True, blank=True)),
                ('version', models.BigIntegerField(null=True, blank=True)),
                ('versionnote', models.CharField(max_length=1000, null=True, blank=True)),
                ('versionstate', models.CharField(max_length=255, choices=[(b'RELEASED', b'RELEASED'), (b'DRAFT', b'DRAFT'), (b'DEACCESSIONED', b'DEACCESSIONED')])),
                ('versionnumber', models.BigIntegerField(null=True, blank=True)),
                ('minorversionnumber', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'datasetversion',
                'managed': False,
            },
        ),
    ]
