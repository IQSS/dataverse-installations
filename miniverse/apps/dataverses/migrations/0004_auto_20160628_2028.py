# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataverses', '0003_citationpagecheck_error_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataverseTheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('backgroundcolor', models.CharField(max_length=255, null=True, blank=True)),
                ('linkcolor', models.CharField(max_length=255, null=True, blank=True)),
                ('linkurl', models.CharField(max_length=255, null=True, blank=True)),
                ('logo', models.CharField(max_length=255, null=True, blank=True)),
                ('logoalignment', models.CharField(max_length=255, null=True, blank=True)),
                ('logobackgroundcolor', models.CharField(max_length=255, null=True, blank=True)),
                ('logoformat', models.CharField(max_length=255, null=True, blank=True)),
                ('tagline', models.CharField(max_length=255, null=True, blank=True)),
                ('textcolor', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'dataversetheme',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='citationpagecheck',
            name='citation_found',
            field=models.BooleanField(default=False),
        ),
    ]
