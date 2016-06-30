# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataverses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataverserole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(unique=True, max_length=255)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('permissionbits', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dataverserole',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createtime', models.DateTimeField()),
                ('name', models.CharField(max_length=255)),
                ('usagecount', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'template',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CitationPageCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('citation_url', models.URLField()),
                ('widget_link', models.TextField(blank=True)),
                ('citation_found', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('dataverse', models.ForeignKey(to='dataverses.Dataverse')),
            ],
            options={
                'ordering': ('-created', 'dataverse'),
            },
        ),
    ]
