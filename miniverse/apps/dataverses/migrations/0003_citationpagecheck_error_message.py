# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataverses', '0002_citationpagecheck_dataverserole_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='citationpagecheck',
            name='error_message',
            field=models.TextField(blank=True),
        ),
    ]
