# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0013_auto_20150908_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='entidade',
            name='nascimento_fundacao',
            field=models.DateField(null=True, verbose_name=b'Nascimento / Funda\xc3\xa7\xc3\xa3o:'),
        ),
    ]
