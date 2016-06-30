# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actionlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actionlogrecord',
            options={'ordering': ('-starttime',), 'managed': False},
        ),
    ]
