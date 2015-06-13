# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_auto_20150611_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=300)),
                ('read', models.BooleanField(default=False)),
                ('slug', models.CharField(default=b'default', max_length=100)),
                ('book', models.ForeignKey(to='main.Book', null=True)),
                ('library', models.ForeignKey(to='main.Library', null=True)),
                ('owner', models.ForeignKey(related_name='owner', to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
