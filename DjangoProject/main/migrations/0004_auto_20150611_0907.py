# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='book',
            field=models.ForeignKey(to='main.Book', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='library',
            field=models.ForeignKey(to='main.Library', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
