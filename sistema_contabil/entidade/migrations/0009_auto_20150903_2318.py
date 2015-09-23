# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0008_municipio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipio',
            name='nome',
            field=models.CharField(max_length=100, verbose_name=b'Munic\xc3\xadpio:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
    ]
