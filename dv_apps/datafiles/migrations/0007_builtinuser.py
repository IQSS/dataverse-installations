# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-23 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datafiles', '0006_datafilecategory_datafiletag_filemetadatadatafilecategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuiltInUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliation', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('encryptedpassword', models.CharField(blank=True, max_length=255, null=True)),
                ('firstname', models.CharField(blank=True, max_length=255, null=True)),
                ('lastname', models.CharField(blank=True, max_length=255, null=True)),
                ('passwordencryptionversion', models.IntegerField(blank=True, null=True)),
                ('position', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'builtinuser',
                'managed': False,
            },
        ),
    ]