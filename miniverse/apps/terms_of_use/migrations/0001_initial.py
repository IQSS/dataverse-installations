# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TermsOfUseAndAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('termsofaccess', models.TextField(null=True, blank=True)),
                ('termsofuse', models.TextField(null=True, blank=True)),
                ('license', models.CharField(max_length=255, null=True, blank=True)),
                ('availabilitystatus', models.TextField(null=True, blank=True)),
                ('citationrequirements', models.TextField(null=True, blank=True)),
                ('conditions', models.TextField(null=True, blank=True)),
                ('confidentialitydeclaration', models.TextField(null=True, blank=True)),
                ('contactforaccess', models.TextField(null=True, blank=True)),
                ('dataaccessplace', models.TextField(null=True, blank=True)),
                ('depositorrequirements', models.TextField(null=True, blank=True)),
                ('disclaimer', models.TextField(null=True, blank=True)),
                ('fileaccessrequest', models.NullBooleanField()),
                ('originalarchive', models.TextField(null=True, blank=True)),
                ('restrictions', models.TextField(null=True, blank=True)),
                ('sizeofcollection', models.TextField(null=True, blank=True)),
                ('specialpermissions', models.TextField(null=True, blank=True)),
                ('studycompletion', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'termsofuseandaccess',
                'managed': False,
            },
        ),
    ]
