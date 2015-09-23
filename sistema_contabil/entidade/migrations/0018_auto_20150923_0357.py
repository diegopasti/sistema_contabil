# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0017_auto_20150917_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidade',
            name='registro_geral',
            field=models.CharField(max_length=12, verbose_name=b'Identidade:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
    ]
