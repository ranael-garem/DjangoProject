# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150611_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.AlterField(
            model_name='notification',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
