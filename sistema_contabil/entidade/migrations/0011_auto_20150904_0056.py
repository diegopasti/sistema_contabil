# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0010_bairro'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bairro',
            unique_together=set([('nome', 'municipio')]),
        ),
    ]
