# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0025_auto_20151002_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entidade',
            name='desabilitado',
        ),
        migrations.AddField(
            model_name='entidade',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
