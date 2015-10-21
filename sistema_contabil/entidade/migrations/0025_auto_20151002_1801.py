# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0024_auto_20150930_2356'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item_protocolo',
            old_name='item',
            new_name='documento',
        ),
        migrations.RenameField(
            model_name='item_protocolo',
            old_name='mes_referencia',
            new_name='referencia',
        ),
        migrations.AlterField(
            model_name='item_protocolo',
            name='complemento',
            field=models.TextField(max_length=500, null=True, verbose_name=b'Descri\xc3\xa7\xc3\xa3o:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
    ]
